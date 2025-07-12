terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

# Cria uma rede para os containers se comunicarem
resource "docker_network" "techagro_network" {
  name = "techagro-local-network"
}

# Cria um volume para persistir os dados do Postgres
resource "docker_volume" "db_data" {
  name = "techagro-pgdata"
}

# Constrói a imagem da API a partir do Dockerfile
resource "docker_image" "techagro_api" {
  name = "techagro-api:latest"
  build {
    context = "${path.cwd}/.." # Sobe um nível para a raiz do projeto
    dockerfile = "Dockerfile"
  }
}

# Container do Banco de Dados (Postgres)
resource "docker_container" "db" {
  name  = "techagro-db"
  image = "postgres:15-alpine"
  
  env = [
    "POSTGRES_USER=postgres",
    "POSTGRES_PASSWORD=postgres",
    "POSTGRES_DB=postgres"
  ]

  volumes {
    volume_name    = docker_volume.db_data.name
    container_path = "/var/lib/postgresql/data"
  }

  ports {
    internal = 5432
    external = 5432
  }

  networks_advanced {
    name = docker_network.techagro_network.name
  }

  restart = "always"
}

# Container da API (Django/Python)
resource "docker_container" "api" {
  name  = "techagro-api"
  image = docker_image.techagro_api.name
  
  command = [
    "sh", "-c",
    "python framework/manage.py migrate && python framework/manage.py runserver 0.0.0.0:8000"
  ]

  volumes {
    host_path      = "${path.cwd}/.."
    container_path = "/app"
  }

  # O Terraform não tem um "env_file" direto.
  # O container irá ler o .env da raiz do projeto, pois o volume está montado.
  
  depends_on = [docker_container.db]

  healthcheck {
    test = ["CMD-SHELL", "pg_isready -U postgres -d postgres"]
    interval = "5s"
    timeout = "5s"
    retries = 5
  }

  networks_advanced {
    name = docker_network.techagro_network.name
  }

  restart = "always"
}

# Container do Nginx
resource "docker_container" "nginx" {
  name  = "techagro-nginx"
  image = "nginx:latest"

  ports {
    internal = 80
    external = 7000
  }

  volumes {
    host_path      = "${path.cwd}/../nginx.conf"
    container_path = "/etc/nginx/nginx.conf"
    read_only      = true
  }

  depends_on = [docker_container.api]

  networks_advanced {
    name = docker_network.techagro_network.name
  }

  restart = "always"
}