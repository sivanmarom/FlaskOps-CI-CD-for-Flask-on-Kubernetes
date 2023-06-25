provider "aws" {
  region = var.region
}

# Create a VPC
resource "aws_vpc" "eks_vpc" {
  cidr_block = var.cidr_block

  tags = {
    Name = var.eks_vpc_name
  }
}

# Fetch available availability zones
data "aws_availability_zones" "available_zones" {}

# Create subnets within the VPC for each availability zone
resource "aws_subnet" "eks_subnet" {
  count = length(data.aws_availability_zones.available_zones.names)

  vpc_id            = aws_vpc.eks_vpc.id
  cidr_block        = "10.0.${count.index}.0/24" # Replace with your desired subnet CIDR block pattern
  availability_zone = data.aws_availability_zones.available_zones.names[count.index]

  tags = {
    Name = "eks-subnet-${count.index + 1}"
  }
}

# Create a security group for the EKS cluster
resource "aws_security_group" "eks_cluster_sg" {
  vpc_id = aws_vpc.eks_vpc.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = var.sg_name
  }
}

# Create the IAM role for the EKS cluster
resource "aws_iam_role" "eks_cluster_role" {
  name = var.eks_cluster_role

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Create the IAM role policy attachment for the EKS cluster
resource "aws_iam_role_policy_attachment" "eks_cluster_policy_attachment" {
  role       = aws_iam_role.eks_cluster_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

# Create the EKS cluster
resource "aws_eks_cluster" "eks_cluster" {
  name     = var.eks_cluster_name
  role_arn = aws_iam_role.eks_cluster_role.arn
  version  = var.eks_cluster_version
  vpc_config {
    subnet_ids         = aws_subnet.eks_subnet[*].id
    security_group_ids = [aws_security_group.eks_cluster_sg.id]
  }

  depends_on = [
    aws_security_group.eks_cluster_sg,
    aws_iam_role_policy_attachment.eks_cluster_policy_attachment
  ]
}
