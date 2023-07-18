import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import boto3
import time
import jenkins
import os
from werkzeug.utils import secure_filename
import tempfile
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

app = Flask(__name__)
my_users = []


# Create AWS clients and resources
s3 = boto3.client("s3")
ec2 = boto3.resource("ec2")
iam = boto3.client("iam")

secret_key = os.urandom(24)
app.secret_key = secret_key


@app.route('/signup', methods=['POST', 'GET'])
def Signup():
    if request.method == 'POST':
        user_name = request.form.get("username")
        password = request.form.get("password")
        my_users.append(user_name)
        return redirect("/registered")
    return render_template("signup.html")


@app.route('/')
def homepage():
    return render_template("homepage.html")


@app.route('/registered')
def registered():
    return render_template("registered.html", my_users=my_users)


@app.route('/aws', methods=['POST', 'GET'])
def create_iam_user():
    if request.method == 'POST' and request.form['submit'] == 'Create user':
        iam = boto3.client("iam")
        username = request.form.get('username')
        password = request.form.get('password')
        iam.create_user(UserName=username)
        iam.add_user_to_group(GroupName='admin_permissions', UserName=username)
        iam.create_login_profile(
            UserName=username, Password=password, PasswordResetRequired=False)
        access_keys = iam.create_access_key(UserName=username)
        access_key_id = access_keys["AccessKey"]["AccessKeyId"]
        secret_access_key = access_keys["AccessKey"]["SecretAccessKey"]
        return redirect(url_for('user_information', username=username, password=password, access_key_id=access_key_id,
                        secret_access_key=secret_access_key))
    elif request.method == 'POST' and request.form['submit'] == 'Create instance':
        launched = launch_instance()
        return render_template("aws.html", instances=launched)
    return render_template("aws.html")


@app.route('/user_created')
def user_information():
    return render_template('iam_creation_user_result.html',
                           username=request.args.get('username'),
                           password=request.args.get('password'),
                           access_key_id=request.args.get('access_key_id'),
                           secret_access_key=request.args.get('secret_access_key'))


def launch_instance():
    ec2 = boto3.resource("ec2")
    add_docker = 'add_docker' in request.form
    add_jenkins = 'add_jenkins' in request.form
    user_data = "#!/bin/bash\n"
    if add_docker:
        user_data += "sudo apt update && sudo apt -y install docker.io\n"
    if add_jenkins:
        user_data += 'docker run --name jenkins_master -p 8080:8080 -p 50000:50000 -d -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts\n'
    instance_name = request.form.get('instance_name')
    instance_type = request.form.get('instance_type')
    key_pair_name = 'project4'
    image_id = request.form.get('image_id')
    security_group_id = 'sg-0450400339dd7cb3e'
    instance_count = int(request.form['instance_count'])
    instances = []
    for i in range(instance_count):
        instance = ec2.create_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            KeyName=key_pair_name,
            SecurityGroupIds=[security_group_id],
            MinCount=instance_count,
            MaxCount=instance_count,
            UserData=user_data,
            TagSpecifications=[{
                'ResourceType': "instance",
                'Tags': [{'Key': 'Name', 'Value': instance_name}]
            }]
        )
        while True:
            instance[i].reload()
            if instance[i].state['Name'] == 'running' and instance[i].public_ip_address is not None:
                break
            print("Waiting for instance to be running and public IP address...")
            time.sleep(5)
        instances.append({
            'instance_name': instance_name,
            'instance_id': instance[i].id,
            'instance_public_ip': instance[i].public_ip_address,
            'instance_state': instance[i].state['Name']
        })
    return instances


@app.route('/docker_image', methods=['POST', 'GET'])
def create_docker_image():
    if request.method == 'POST':
        image_name = request.form.get('image_name')
        session['image_name'] = image_name
        subprocess.run(['docker', 'build', '-t',
                       f'{image_name}', '-f', 'hello/Dockerfile', 'hello'])
        subprocess.run(
            ['docker', 'tag', f'{image_name}', f'sivanmarom/test:{image_name}'])
        subprocess.run(
            ['docker', 'login', '-u', 'sivanmarom', '-p', 'sm5670589'])
        subprocess.run(['docker', 'push', f'sivanmarom/test:{image_name}'])

        return redirect(url_for('create_jenkins_job_pipeline'))
    else:
        return render_template('docker_image.html')


@app.route('/jenkins_job/freestyle', methods=['POST', 'GET'])
def create_jenkins_job_freestyle():
    if request.method == "POST":
        job_name = request.form.get("job_test")
        jenkins_url = request.form.get("jenkins_url")
        server = jenkins.Jenkins(
            jenkins_url, username='sivan_marom', password='1234')
        with open('infra_flask_app/templates/jenkins_job.xml', 'r') as f:
            job_config_xml = f.read()
        server.create_job(job_name, job_config_xml)
        server.build_job(job_name)
        return "job created successfully"
    return render_template('jenkins_job.html')


@app.route('/jenkins_job/pipeline', methods=['POST', 'GET'])
def create_jenkins_job_pipeline():
    if request.method == "POST":
        job_name = request.form.get("job2")
        jenkins_url = request.form.get("jenkins_url")
        image_name = session.get('image_name')
        image_dict = {'image_name': image_name}
        workspace = request.form.get('workspace')
        if workspace == 'Testing':
            with open('infra_flask_app/templates/jenkins_job_test.xml', 'r') as f:
                job_config_xml = f.read()
        elif workspace == 'Production':
            with open('infra_flask_app/templates/jenkins_job_pipeline_deploy.xml', 'r') as f:
                job_config_xml = f.read()
        server = jenkins.Jenkins(
            jenkins_url, username='sivan_marom', password='1234')
        server.create_job(job_name, job_config_xml)
        server.build_job(job_name, parameters=image_dict)
        return "Job created successfully"
    return render_template('jenkins_job.html')


def create_user(username: str, password: str, full_name: str, email: str, jenkins_url: str):
    jenkins_admin_username = "sivan_marom"
    # Replace with your Jenkins API Token
    jenkins_api_token = "114af544a4188b2e7bbee9396f400a4e4a"
    create_user_url = f"{jenkins_url}securityRealm/createAccountByAdmin"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {jenkins_api_token}"
    }
    data = {
        "username": username,
        "password1": password,
        "password2": password,
        "fullname": full_name,
        "email": email,
        "jenkins.security.ApiTokenProperty": True
    }

    response = requests.post(create_user_url, headers=headers, data=data, auth=HTTPBasicAuth(
        jenkins_admin_username, jenkins_api_token))

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        error_div = soup.find('div', class_='error')
        if error_div:
            error_message = error_div.text.strip()
            return {
                "success": False,
                "message": f"Error creating user '{username}': {error_message}"
            }
        else:
            return {
                "success": True,
                "message": f"User '{username}' created successfully.",
                "statusCode:": response.status_code
            }
    else:
        return {
            "success": False,
            "message": f"Error creating user '{username}': {response.text}",
            "statusCode:": response.status_code
        }


def jenkins_user_assign_roles(username: str, jenkins_url: str):
    new_role = 'admin'
    jenkins_admin_username = "sivan_marom"
    # Replace with your Jenkins API Token
    jenkins_api_token = "114af544a4188b2e7bbee9396f400a4e4a"
    assign_role_url = f"{jenkins_url}role-strategy/strategy/assignRole"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {jenkins_api_token}"
    }
    data = {
        "type": "globalRoles",
        "roleName": new_role,
        "sid": username
    }

    response = requests.post(assign_role_url, headers=headers, data=data, auth=HTTPBasicAuth(
        jenkins_admin_username, jenkins_api_token))

    if response.status_code == 200:
        return {
            "success": True,
            "message": f"Role '{new_role}' assigned to user '{username}' successfully.",
            "statusCode": response.status_code
        }
    else:
        return {
            "success": False,
            "message": f"Error assigning role '{new_role}' to user '{username}': {response.text}",
            "statusCode": response.status_code
        }


@app.route('/create_jenkins_user', methods=['POST', 'GET'])
def create_jenkins_user():
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        jenkins_url = request.form.get('jenkins_url')

        user_creation_result = create_user(
            new_username, new_password, full_name, email, jenkins_url)
        if user_creation_result["success"]:
            user_assign_roles_result = jenkins_user_assign_roles(
                new_username, jenkins_url)
            if user_assign_roles_result["success"]:
                return "Jenkins user created and assigned role successfully"
            else:
                return f"Error assigning role to user: {user_assign_roles_result['message']}"
        else:
            return f"Error creating Jenkins user: {user_creation_result['message']}"

    return render_template('create_jenkins_user.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
