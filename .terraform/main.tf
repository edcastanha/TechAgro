resource "google_project" "project" {
  project_id = var.project_id
  # Opcional: Adicione um nome para o projeto se for criar um novo, ou remova se o projeto já existe
  # name       = "Meu Projeto Agri Django"
}

# Configura o provedor Google Cloud
provider "google" {
  project = var.project_id
  region  = var.region
}

# Habilita as APIs necessárias
resource "google_project_service" "enabled_apis" {
  for_each = toset([
    "run.googleapis.com",
    "sqladmin.googleapis.com",
    "servicenetworking.googleapis.com", # Necessário para IP Privado do Cloud SQL
    "artifactregistry.googleapis.com",   # Se você usar o Artifact Registry para suas imagens Docker
    "storage.googleapis.com",            # Para Cloud Storage
  ])
  project            = var.project_id
  service            = each.key
  disable_on_destroy = false # Mantenha as APIs ativadas mesmo se o Terraform for destruído
}

---

### **Recurso: Cloud SQL (PostgreSQL)**

```terraform
# Instância do Cloud SQL
resource "google_sql_database_instance" "postgres_instance" {
  database_version = "POSTGRES_14" # Ou a versão que preferir
  name             = var.db_instance_name
  project          = var.project_id
  region           = var.region
  settings {
    tier = "db-f1-micro" # Tier de menor custo para desenvolvimento/início
    ip_configuration {
      ipv4_enabled = true
      private_network_config { # Opcional, mas recomendado para segurança e desempenho com Cloud Run
        network = "projects/${var.project_id}/global/networks/default" # Sua rede VPC padrão
        # Adicione `enable_private_ip = true` na configuração da rede, se necessário
      }
    }
    backup_configuration {
      enabled            = true
      binary_log_enabled = false
      start_time         = "03:00"
    }
    disk_size = 20 # GB, tamanho mínimo para f1-micro
    disk_type = "SSD"
  }
  # Garante que as APIs estejam habilitadas antes de criar a instância SQL
  depends_on = [google_project_service.enabled_apis]
}

# Banco de dados dentro da instância
resource "google_sql_database" "database" {
  instance = google_sql_database_instance.postgres_instance.name
  name     = var.db_database_name
  project  = var.project_id
  charset  = "UTF8"
  collation = "C"
}

# Usuário do banco de dados
resource "google_sql_user" "db_user" {
  instance = google_sql_database_instance.postgres_instance.name
  name     = var.db_user
  password = var.db_password
  host     = "%" # Permite conexão de qualquer host. Para maior segurança, restrinja isso.
  project  = var.project_id
}