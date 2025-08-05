⸻

🚀 FlaskOps – CI/CD for Flask on Kubernetes

FlaskOps is a full-stack DevOps project that demonstrates end-to-end CI/CD automation for deploying a Flask application on Kubernetes (EKS). It showcases the use of Jenkins, Terraform, Docker, Helm, Prometheus, Grafana, and HPA to manage, monitor, and scale a cloud-native app.

⸻

🧩 Project Goals • Automate the full development lifecycle: build → test → deploy → monitor. • Apply Infrastructure-as-Code using Terraform & Kubernetes. • Implement auto-scaling, observability, and production-grade CI/CD pipelines. • Showcase DevOps skills across multiple platforms & tools.

⸻

🔧 Tech Stack

Category Technology Details App Flask (Python) REST API + Docker CI/CD Jenkins Multi-stage pipeline IaC Terraform AWS EKS provisioning (incl. IAM, EC2) Container Docker App containerization Orchestration Kubernetes (EKS) Cluster on AWS Deployment Helm Helm chart for rollout/versioning Monitoring Prometheus & Grafana Via Docker Compose Auto-scaling Kubernetes HPA Horizontal Pod Autoscaler Storage AWS S3 + DynamoDB Test reports and logs Testing Selenium Automated UI testing

⸻

🌟 Features

✅ End-to-end CI/CD pipeline with Jenkins ✅ Infrastructure provisioning via Terraform ✅ Docker image builds + push to DockerHub ✅ Helm-based deployment to Kubernetes ✅ Live monitoring with Prometheus + Grafana ✅ Auto-scaling via HPA based on CPU usage ✅ Test results stored in AWS (S3 + DynamoDB)

⸻

🗂️ Folder Structure

FlaskOps/ ├── infra_flask_app/ # Flask Infra backend app (runs inside Jenkins Agent) ├── terraform/ # Terraform for AWS resources (EKS, EC2, IAM, etc.) ├── jenkins_files/ # Jenkins pipeline definitions ├── k8s/mychart/ # Helm chart for deployment ├── monitoring/ # Prometheus + Grafana via Docker Compose ├── tests/ # Selenium tests ├── Dockerfiles/ # Docker configs for all services └── README.md

⸻

🧭 Architecture Diagram

WhatsApp Image 2025-08-05 at 11 40 44

⸻

🚀 Getting Started 1. Clone the repo

git clone https://github.com/sivanmarom/FlaskOps-Orchestrating-Flask-Applications-on-Kubernetes.git cd FlaskOps-Orchestrating-Flask-Applications-on-Kubernetes

2.	Install dependencies
•	Jenkins
•	Docker
•	Terraform
•	Helm
•	AWS CLI configured with proper IAM permissions
•	Prometheus & Grafana via Docker Compose
3.	Run Jenkins Jobs
•	🔧 infra_flask_app – builds Docker image, runs tests, pushes image
•	🚀 deploy_job – deploys to Kubernetes using Helm
•	📊 Access monitoring dashboards on http://localhost:3000 (Grafana)
⸻

⚙️ Automation Flow 1. Terraform provisions AWS infrastructure: EKS, S3, DynamoDB 2. Jenkins builds + tests Flask app (Selenium) 3. Docker image is pushed to DockerHub 4. Helm deploys app to EKS 5. Prometheus scrapes metrics → Grafana visualizes them 6. HPA monitors CPU and scales pods as needed

⸻

📈 Monitoring & Scaling • 📊 Grafana Dashboard: Tracks CPU usage, requests, and pod count • 📡 Prometheus Alerts: Resource usage + performance metrics • 🔁 HPA (Horizontal Pod Autoscaler): Auto-adjusts pods based on CPU

⸻

🧪 Example Selenium Test Output

Test reports are uploaded to AWS S3 and indexed in DynamoDB

⸻

🤝 Contributing

Contributions are welcome!

git fork git checkout -b feature/my-feature git commit -m "Add new feature" git push origin feature/my-feature open a Pull Request

⸻

📬 Contact

Sivan Marom 📧 sivmarom@gmail.com 
🔗 LinkedIn Profile www.linkedin.com/in/sivan-marom 
