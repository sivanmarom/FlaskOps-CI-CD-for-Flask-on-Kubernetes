import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import boto3
import time
import jenkins
import os
app = Flask(__name__)
my_users = []


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
    key_pair_name = 'jenkins-master'
    image_id = request.form.get('image_id')
    security_group_id = 'sg-03915679baa198009'
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


@app.route('/user_created')
def user_information():
    return render_template('iam_creation_user_result.html',
                           username=request.args.get('username'),
                           password=request.args.get('password'),
                           access_key_id=request.args.get('access_key_id'),
                           secret_access_key=request.args.get('secret_access_key'))


@app.route('/docker_image', methods=['POST', 'GET'])
def create_docker_image():
    if request.method == 'POST':
        image_name = request.form.get('image_name')
        subprocess.run(['docker', 'build', '-t', f'{image_name}', '.'])
        subprocess.run(
            ['docker', 'tag', f'{image_name}', f'sivanmarom/test:{image_name}'])
        subprocess.run(['docker', 'login', '-u', 'sivanmarom', '-p', ''])
        subprocess.run(['docker', 'push', f'sivanmarom/test:{image_name}'])
        return f'Docker image {image_name} created and pushed to Docker Hub'
    else:
        return render_template('docker_image.html')


@app.route('/create_jenkins_user', methods=['POST', 'GET'])
def create_jenkins_user():
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        jenkins_url = request.form.get('jenkins_url')
        jar_filename = 'jenkins-cli.jar'
        jar_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), jar_filename)
        java_path = r'C:\Program Files\Java\jdk-11\bin\java'

        command = f'echo \'jenkins.model.Jenkins.instance.securityRealm.createAccount("{new_username}", "{new_password}", "{full_name}", "{email}")\' | "{java_path}" -jar "{jar_path}" -s "{jenkins_url}" groovy ='
        subprocess.run(command, shell=True)

        return "Jenkins user created successfully"

    return render_template('jenkins_user.html')


@app.route('/jenkins_job/freestyle', methods=['POST', 'GET'])
def create_jenkins_job_freestyle():
    if request.method == "POST":
        job_name = request.form.get("job_test")
        jenkins_url = request.form.get("jenkins_url")
        server = jenkins.Jenkins(
            jenkins_url, username='sivan_marom', password='1234')
        with open('templates/jenkins_job.xml', 'r') as f:
            job_config_xml = f.read()
        server.create_job(job_name, job_config_xml)
        server.build_job(job_name)
        return "job created successfully"
    return render_template('jenkins_job.html')


@app.route('/jenkins_job/pipeline', methods=['POST', 'GET'])
def create_jenkins_job_pipeline():
    if request.method == "POST":
        job_name = request.form.get("job2")
        server = jenkins.Jenkins(
            'http://23.22.159.73:8080/', username='sivan_marom', password='1234')
        workspace = request.form.get('workspace')
        if workspace == 'Testing':
            with open('templates/jenkins_job_pipeline.xml', 'r') as f:
                job_config_xml = f.read()
        elif workspace == 'Production':
            with open('templates/jenkins_job_pipeline_production.xml', 'r') as f:
                job_config_xml = f.read()
        server.create_job(job_name, job_config_xml)
        server.build_job(job_name)
        return "job created successfully"
    return render_template('jenkins_job.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
