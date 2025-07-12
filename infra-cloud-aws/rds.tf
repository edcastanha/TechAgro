resource "aws_db_subnet_group" "default" {
  name       = "${var.environment}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name        = "${var.environment}-db-subnet-group"
    Environment = var.environment
    Project     = "TechAgro"
  }
}

resource "aws_security_group" "db" {
  name        = "${var.environment}-db-sg"
  description = "Allow inbound traffic from the application security group"
  vpc_id      = aws_vpc.main.id

  # A regra de entrada será adicionada no arquivo ecs.tf para evitar dependência cíclica

  tags = {
    Name        = "${var.environment}-db-sg"
    Environment = var.environment
    Project     = "TechAgro"
  }
}

resource "random_password" "db_password" {
  length  = 16
  special = true
}

resource "aws_secretsmanager_secret" "db_credentials" {
  name = "${var.environment}/techagro/db/credentials"
  description = "Database credentials for TechAgro"
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = var.db_username
    password = random_password.db_password.result
    engine   = "postgres"
    host     = aws_db_instance.main.address
    port     = aws_db_instance.main.port
    dbname   = var.db_name
  })

  depends_on = [aws_db_instance.main]
}

resource "aws_db_instance" "main" {
  identifier             = "${var.environment}-techagro-db"
  allocated_storage      = 20
  storage_type           = "gp2"
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = var.db_instance_class
  db_name                = var.db_name
  username               = var.db_username
  password               = random_password.db_password.result
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.db.id]
  skip_final_snapshot    = true # Para dev/teste. Mudar para false em produção.

  tags = {
    Environment = var.environment
    Project     = "TechAgro"
  }
}
