variable "infra_flask_bucket" {
  type    = string
  default = "infra-flask-bucket"
}

variable "flask_app_bucket" {
  type    = string
  default = "hello-user-bucket"
}

variable "region" {
  type    = string
  default = "us-west-2"
}
