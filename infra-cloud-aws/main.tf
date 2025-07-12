# Repositório para armazenar a imagem Docker da aplicação
resource "aws_ecr_repository" "api" {
  name                 = "${var.environment}-techagro-api"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Environment = var.environment
    Project     = "TechAgro"
  }
}
