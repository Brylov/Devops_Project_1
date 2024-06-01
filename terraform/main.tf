provider "aws" {
  region = "us-east-1"  # Specify your desired AWS region
}

resource "aws_ecr_repository" "portfolio_mongodb" {
  name                 = "portfolio-mongodb"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "portfolio_backend" {
  name                 = "portfolio-backend"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "portfolio_frontend" {
  name                 = "portfolio-frontend"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}

output "portfolio_mongodb_repository_url" {
  value = aws_ecr_repository.portfolio_mongodb.repository_url
}

output "portfolio_backend_repository_url" {
  value = aws_ecr_repository.portfolio_backend.repository_url
}

output "portfolio_frontend_repository_url" {
  value = aws_ecr_repository.portfolio_frontend.repository_url
}