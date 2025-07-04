# Variáveis de configuração do projeto Google Cloud
variable "project_id" {
  description = "O ID do seu projeto Google Cloud."
  type        = string
}

variable "region" {
  description = "A região do Google Cloud para implantar os recursos."
  type        = string
  default     = "us-central1" # Exemplo: us-central1, southamerica-east1
}

# Variáveis do Cloud SQL
variable "db_instance_name" {
  description = "Nome da instância do Cloud SQL."
  type        = string
  default     = "django-agri-pg"
}

variable "db_database_name" {
  description = "Nome do banco de dados PostgreSQL."
  type        = string
  default     = "agri_db"
}

variable "db_user" {
  description = "Usuário do banco de dados PostgreSQL."
  type        = string
  default     = "django_user"
}

variable "db_password" {
  description = "S"
  type        = string
  sensitive   = true # Marca a variável como sensível para não ser exibida em logs
}

# Variáveis do Cloud Run
variable "cloud_run_service_name" {
  description = "Tech Agro API."
  type        = string
  default     = "agri-api-django"
}

variable "docker_image_name" {
  description = "Nome da imagem Docker da sua aplicação Django (ex: gcr.io/<PROJECT_ID>/<IMAGE_NAME>)."
  type        = string
}

# Variáveis do Cloud Storage para arquivos estáticos/media
variable "gcs_bucket_name" {
  description = "Nome do bucket do Cloud Storage para arquivos estáticos e de mídia."
  type        = string
}