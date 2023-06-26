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
  name               = "eks-cluster-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
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
    aws_security_group.eks_cluster_sg
  ]
}
# Create the IAM policy for the EKS cluster
resource "aws_iam_policy" "eks_cluster_policy" {
  name   = "eks-cluster-policy"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["eks:DescribeCluster"],
      "Resource": ["arn:aws:eks:${var.region}:${var.account_id}:cluster/${aws_eks_cluster.eks_cluster.name}"]
    },
    {
      "Effect": "Allow",
      "Action": ["ec2:DescribeInstances"],
      "Resource": "*"
    }
  ]
}
EOF
}
# Attach the IAM policy to the IAM role
resource "aws_iam_role_policy_attachment" "eks_cluster_policy_attachment" {
  role       = aws_iam_role.eks_cluster_role.name
  policy_arn = aws_iam_policy.eks_cluster_policy.arn
}


# Create the EKS node group
resource "aws_eks_node_group" "eks_node_group" {
  cluster_name    = aws_eks_cluster.eks_cluster.name
  node_group_name = "flask-nodes"
  node_role_arn   = aws_iam_role.eks_cluster_role.arn
  subnet_ids      = aws_subnet.eks_subnet[*].id

  scaling_config {
    desired_size = 3
    min_size     = 1
    max_size     = 5
  }

  instance_types = ["t2.micro"]

  depends_on = [
    aws_eks_cluster.eks_cluster
  ]
}
