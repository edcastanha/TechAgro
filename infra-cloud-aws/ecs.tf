resource "aws_ecs_cluster" "main" {
  name = "${var.environment}-techagro-cluster"

  tags = {
    Name        = "${var.environment}-techagro-cluster"
    Environment = var.environment
    Project     = "TechAgro"
  }
}

# IAM Role para as tarefas ECS
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.environment}-ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ],
  })

  tags = {
    Name        = "${var.environment}-ecs-task-execution-role"
    Environment = var.environment
    Project     = "TechAgro"
  }
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "ecs_secrets_manager_access" {
  name = "${var.environment}-ecs-secrets-manager-access"
  role = aws_iam_role.ecs_task_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = aws_secretsmanager_secret.db_credentials.arn
      },
    ],
  })
}

# Security Group para o Load Balancer
resource "aws_security_group" "alb" {
  name        = "${var.environment}-alb-sg"
  description = "Allow HTTP/HTTPS traffic to ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.environment}-alb-sg"
    Environment = var.environment
    Project     = "TechAgro"
  }
}

# Security Group para as tarefas ECS (API)
resource "aws_security_group" "ecs_tasks" {
  name        = "${var.environment}-ecs-tasks-sg"
  description = "Allow traffic from ALB and egress to DB"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 8000 # Porta da sua aplicação Django
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port       = 5432 # Porta do Postgres
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.db.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.environment}-ecs-tasks-sg"
    Environment = var.environment
    Project     = "TechAgro"
  }
}

# Adiciona regra de entrada no SG do DB para permitir tráfego do SG das tarefas ECS
resource "aws_security_group_rule" "db_ingress_from_ecs" {
  type              = "ingress"
  from_port         = 5432
  to_port           = 5432
  protocol          = "tcp"
  security_group_id = aws_security_group.db.id
  source_security_group_id = aws_security_group.ecs_tasks.id
}

# Load Balancer
resource "aws_lb" "main" {
  name               = "${var.environment}-techagro-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  tags = {
    Name        = "${var.environment}-techagro-alb"
    Environment = var.environment
    Project     = "TechAgro"
  }
}

resource "aws_lb_target_group" "api" {
  name        = "${var.environment}-techagro-api-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    path                = "/health/" # Assumindo que você terá um endpoint de health check
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }

  tags = {
    Name        = "${var.environment}-techagro-api-tg"
    Environment = var.environment
    Project     = "TechAgro"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }
}

# ECS Task Definition
resource "aws_ecs_task_definition" "api" {
  family                   = "${var.environment}-techagro-api-task"
  cpu                      = "256"
  memory                   = "512"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn # Usando a mesma role para execução e tarefa

  container_definitions = jsonencode([
    {
      name        = "techagro-api"
      image       = "${aws_ecr_repository.api.repository_url}:latest"
      cpu         = 256
      memory      = 512
      essential   = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        },
      ]
      environment = [
        {
          name  = "DJANGO_SETTINGS_MODULE"
          value = "framework.config.settings"
        },
        {
          name  = "DATABASE_URL"
          value = "postgresql://${var.db_username}:${random_password.db_password.result}@${aws_db_instance.main.address}:${aws_db_instance.main.port}/${var.db_name}"
        }
      ]
      secrets = [
        {
          name      = "DB_PASSWORD"
          valueFrom = "${aws_secretsmanager_secret.db_credentials.arn}:password::"
        },
        {
          name      = "DB_USERNAME"
          valueFrom = "${aws_secretsmanager_secret.db_credentials.arn}:username::"
        },
        {
          name      = "DB_HOST"
          valueFrom = "${aws_secretsmanager_secret.db_credentials.arn}:host::"
        },
        {
          name      = "DB_PORT"
          valueFrom = "${aws_secretsmanager_secret.db_credentials.arn}:port::"
        },
        {
          name      = "DB_NAME"
          valueFrom = "${aws_secretsmanager_secret.db_credentials.arn}:dbname::"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/techagro-api"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    },
  ])

  tags = {
    Name        = "${var.environment}-techagro-api-task"
    Environment = var.environment
    Project     = "TechAgro"
  }
}

# CloudWatch Log Group para as tarefas ECS
resource "aws_cloudwatch_log_group" "api" {
  name              = "/ecs/techagro-api"
  retention_in_days = 7 # Ajuste conforme sua necessidade

  tags = {
    Name        = "${var.environment}-techagro-api-logs"
    Environment = var.environment
    Project     = "TechAgro"
  }
}

# ECS Service
resource "aws_ecs_service" "api" {
  name            = "${var.environment}-techagro-api-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 1 # Pode ser ajustado para escalabilidade
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "techagro-api"
    container_port   = 8000
  }

  depends_on = [
    aws_lb_listener.http,
    aws_iam_role_policy_attachment.ecs_task_execution_role_policy,
    aws_iam_role_policy.ecs_secrets_manager_access
  ]

  tags = {
    Name        = "${var.environment}-techagro-api-service"
    Environment = var.environment
    Project     = "TechAgro"
  }
}
