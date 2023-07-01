variable "region" {
  type    = string
  default = "us-west-2"
}

variable "instnace_type" {
  type    = string
  default = "t3.large"
}

variable "instance_ami" {
  type    = string
  default = "ami-0c65adc9a5c1b5d7c"
}

variable "jenkisn_master_instance" {
  type    = string
  default = "Jenkins_master"
}
variable "security_group" {
  type    = string
  default = "sg-0450400339dd7cb3e"
}

