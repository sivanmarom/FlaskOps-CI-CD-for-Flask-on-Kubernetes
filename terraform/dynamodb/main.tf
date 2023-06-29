provider "aws" {
  region = var.region
}

resource "aws_dynamodb_table" "flask-app-table" {
  name         = var.flask_app_table
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = var.user_col

  attribute {
    name = var.user_col
    type = "S"
  }
  attribute {
    name = var.timestamp_col
    type = "S"
  }
  attribute {
    name = var.message_col
    type = "S"
  }
  global_secondary_index {
    name            = "GSI"
    hash_key        = var.timestamp_col
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "GSI2"
    hash_key        = var.message_col
    projection_type = "ALL"
  }
  tags = {
    Name = var.user_col
  }
}


resource "aws_dynamodb_table" "flask-app-table" {
  name         = var.infra_flask_table
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = var.user_col

  attribute {
    name = var.user_col
    type = "S"
  }
  attribute {
    name = var.timestamp_col
    type = "S"
  }
  attribute {
    name = var.message_col
    type = "S"
  }
  global_secondary_index {
    name            = "GSI"
    hash_key        = var.timestamp_col
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "GSI2"
    hash_key        = var.message_col
    projection_type = "ALL"
  }
  tags = {
    Name = var.user_col
  }
}

output "flask_app_table_name" {
  value = aws_dynamodb_table.flask-app-table.name
}
output "infra_flask_table_name" {
  value = aws_dynamodb_table.infra_flask_table.name
}
