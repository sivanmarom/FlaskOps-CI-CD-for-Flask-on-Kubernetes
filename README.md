# FlaskOps: Orchestrating Flask Applications on Kubernetes

Welcome to FlaskOps, a DevOps project that aims to automate the deployment and management of Flask applications on Kubernetes. This project utilizes various technologies and tools, including Terraform, AWS, Python, Docker, Jenkins, Helm, Prometheus, Grafana, and Kubernetes Horizontal Pod Autoscaler (HPA), to streamline the entire development and deployment lifecycle.

## Project Overview

The project is composed of the following components:

1. Jenkins Master: Responsible for managing and coordinating Jenkins jobs.
2. Jenkins Agent: Communicates with the Jenkins Master and executes jobs, including the creation of the EKS (Elastic Kubernetes Service) cluster.
3. Infra Flask App: An infrastructure Flask application running as a container on the Jenkins Agent. It handles several tasks:

&#8226; Building a Docker image of the Flask app.

&#8226; Creating test jobs to verify the Flask app's functionality.

&#8226; Deploying the Flask app to the Kubernetes cluster.

&#8226; Additional functionality for creating EC2 instances, IAM users, Jenkins jobs (pipeline and freestyle), and Jenkins users.

4. Kubernetes Cluster: The Jenkins Agent creates a Kubernetes cluster with three worker nodes using Terraform. The Kubernetes cluster is provisioned using Terraform code.
5. Flask App: After successful testing, the Flask app is deployed within the Kubernetes cluster.
6. Helm: Helm is used to package and deploy the Flask app as a Helm chart to the Kubernetes cluster, simplifying application management and version control.
7. Prometheus & Grafana: Local instances for monitoring. Prometheus collects metrics from the Flask app running in the EKS cluster, and Grafana provides data visualization for monitoring and analyzing metrics, including CPU usage. The monitoring setup is orchestrated using Docker Compose.
8. Autoscaling using HPA: A Kubernetes Horizontal Pod Autoscaler (HPA) component that automatically scales the number of pods based on CPU utilization. The HPA adjusts the number of pods for the Flask app based on resource utilization.

## Testing, Deployment and Lifecycle Management

The deployment and lifecycle management of the applications are orchestrated using Jenkins pipeline jobs. The Jenkins pipeline includes the following stages:

1. The test job provisions necessary resources using Terraform, such as an S3 bucket and a DynamoDB table.
2. The Flask app's functionality is tested using Selenium, and the test results are uploaded to the S3 bucket and DynamoDB table.
3. The Docker image created by the infrastructure code (after testing) is pushed to Dockerhub.
4. The same image tag used in the test job is used in the deployment job, which deploys the Flask app to the Kubernetes cluster.
5. The Helm chart for the Flask app is packaged and deployed to the Kubernetes cluster using Helm.
6. Autoscaling Deployment: The Kubernetes Horizontal Pod Autoscaler (HPA) component is integrated into the deployment process. It automatically adjusts the number of pods for the Flask app based on CPU utilization. As the application's load increases, the HPA dynamically scales up the number of pods to meet the demand, ensuring optimal performance and resource utilization.

## Getting started

To get started with FlaskOps, follow these steps:

1. Clone this repository to your local environment.
2. Install Jenkins on your machine and set up the Jenkins Master.
3. Install Docker on your machine for local monitoring with Prometheus and Grafana.
4. Install Terraform on your machine for infrastructure provisioning.
5. Set up your AWS credentials to allow Jenkins to interact with AWS resources.
6. Create a Jenkins Agent (Slave) that will execute the Jenkins jobs.
7. Configure the Jenkins Agent to have the necessary permissions to perform tasks like creating the EKS cluster and creating EC2 instances.
8. Install Helm on your machine for packaging and deploying the Flask app.
9. Set up Docker Compose to run Prometheus and Grafana locally for monitoring.
10. Ensure Kubernetes is properly installed and configured on the Jenkins Agent for cluster creation.
11. Customize the Jenkins jobs to match your specific requirements.

## Usage

To use FlaskOps, follow these steps:

1. Run the Jenkins job responsible for creating the EKS cluster.
2. Trigger the Infra Flask App job to build the Docker image, run tests, and deploy the Flask app to the Kubernetes cluster using Helm.
3. Access the Prometheus and Grafana dashboards to monitor the Flask app's performance and CPU usage.
4. The Kubernetes HPA will automatically scale the number of pods based on CPU utilization.

## Conclusion

FlaskOps showcases the power of DevOps automation by integrating various tools and technologies to streamline the deployment and management of Flask applications on Kubernetes. Feel free to explore, customize, and expand this project according to your unique requirements. Happy FlaskOps-ing!

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch: git checkout -b new-feature.
3. Make your changes and commit them: git commit -m 'Add some feature'.
4. Push your changes to the branch: git push origin new-feature.
5. Submit a pull request detailing your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

If you have any questions, suggestions, or feedback, please feel free to contact Sivan Marom at sivmarom@gmail.com.
