variable "region" {
  type    = string
  default = "us-west-2"
}

variable "flask_app_table" {
  type    = string
  default = "flask-app-table"
}

variable "infra_flask_table" {
  type    = string
  default = "infra-flask-table"
}

variable "user_col" {
  type    = string
  default = "User"
}

variable "timestamp_col" {
  type    = string
  default = "TimeStamp"
}

variable "message_col" {
  type    = string
  default = "Message"
}
