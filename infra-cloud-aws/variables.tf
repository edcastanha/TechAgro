variable "environment" {
  description = "O ambiente de implantação (ex: dev, prod)."
  type        = string
}

variable "aws_region" {
  description = "A região da AWS para implantar os recursos."
  type        = string
}

variable "db_username" {
  description = "O nome de usuário para o banco de dados RDS."
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "O nome do banco de dados RDS."
  type        = string
}

variable "db_instance_class" {
  description = "A classe de instância para o banco de dados RDS."
  type        = string
  default     = "db.t3.micro"
}