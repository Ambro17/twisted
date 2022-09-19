terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
  required_version = ">= 0.14.9"
  backend "s3" {
    bucket = "twisted-terraform"
    key    = "terraform.tfstate"
    region = "us-east-1"     
    dynamodb_table = "terraform-state" # Store a lock on each terraform write operation to avoid race conditions
  }
}

provider "aws" {
  profile = "personal"
  region  = "us-east-1"
}
