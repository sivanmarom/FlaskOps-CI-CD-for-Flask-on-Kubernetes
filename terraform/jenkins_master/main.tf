provider "aws" {
  region = var.region
}

resource "aws_instance" "Jenkins_master" {
  ami                    = var.instance_ami
  instance_type          = var.instnace_type
  vpc_security_group_ids = [var.security_group]
  key_name               = "project4"

  connection {
    type        = "ssh"
    host        = self.public_ip
    user        = "ubuntu"
    private_key = file("${path.module}/project4.pem")
    timeout     = "10m"
  }
  tags = {
    Name = var.jenkisn_master_instance
  }

  lifecycle {
    create_before_destroy = true
  }
  provisioner "remote-exec" {
    inline = [
      "sudo apt update -y",
      "sudo apt -y install docker.io",
      "sudo apt install -y default-jdk",
      "sudo apt install -y python3",
      "curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null",
      "echo 'deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/' | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null",
      "sudo apt-get update -y",
      "sudo apt-get install -y jenkins",
      "systemctl start jenkins.service",
      "sudo apt-get update -y && sudo apt-get install -y gnupg software-properties-common",
      "wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg",
      "gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint",
      "echo 'deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main' | sudo tee /etc/apt/sources.list.d/hashicorp.list",
      "sudo apt update -y",
      "sudo install -y terraform --classic",
      "sudo apt install -y unzip",
      "curl -o awscliv2.zip https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip",
      "unzip awscliv2.zip",
      "sudo ./aws/install",
      "sudo snap install kubectl --classic",
      "curl --silent --location 'https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz' | tar xz -C /tmp",
      "sudo mv /tmp/eksctl /usr/local/bin"
    ]
  }
}
