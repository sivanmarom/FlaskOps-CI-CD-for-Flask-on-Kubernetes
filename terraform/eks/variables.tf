variable "region" {
  type    = string
  default = "us-west-2"
}

variable "cidr_block" {
  type    = string
  default = "10.0.0.0/16"
}

variable "eks_vpc_name" {
  type    = string
  default = "eks-vpc"
}

variable "sg_name" {
  type    = string
  default = "eks-cluster-sg"
}
variable "infra_cluster_name" {
  type    = string
  default = "infra-cluster"
}
variable "flask_cluster_name" {
  type    = string
  default = "flask-cluster"
}
#mabey upgrade version
variable "eks_cluster_version" {
  type    = string
  default = "1.26"
}

variable "eks_cluster_role" {
  type    = string
  default = "eks-cluster-role"
}

variable "account_id" {
  type    = string
  default = "676000770422"
}


