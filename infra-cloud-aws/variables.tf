variable "bucket_name" {
  description = "The name of the S3 bucket for the Terraform backend."
  type        = string
}

variable "environment" {
  description = "The deployment environment (e.g., dev, prod)."
  type        = string
  default     = "dev"
}

variable "db_instance_class" {
  description = "The instance class for the RDS database."
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "The name of the database."
  type        = string
  default     = "techagro"
}

variable "db_username" {
  description = "The master username for the database."
  type        = string
  default     = "postgres"
}

variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "sa-east-1"
}
