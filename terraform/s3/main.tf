provider "aws" {
  region = var.region

}
resource "aws_s3_bucket" "flask-app-bucket" {
  bucket = var.flask_app_bucket
  tags = {
    Name = var.flask_app_bucket
  }
}
resource "aws_s3_bucket_public_access_block" "public_bucket" {
  bucket                  = aws_s3_bucket.flask-app-bucket.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket" "infra-flask-bucket" {
  bucket = var.infra_flask_bucket
  tags = {
    Name = var.infra_flask_bucket
  }
}
resource "aws_s3_bucket_public_access_block" "public_bucket" {
  bucket                  = aws_s3_bucket.infra-flask-bucket.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}


output "flask_app_bucket_name" {
  value = aws_s3_bucket.flask-app-bucket.bucket
}

output "infra_flask_bucket_name" {
  value = aws_s3_bucket.infra-flask-bucket.bucket
}
