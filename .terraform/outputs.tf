output "cloud_run_url" {
  description = "URL do serviço Cloud Run."
  value       = google_cloud_run_service.django_api_service.status[0].url
}

output "db_connection_name" {
  description = "Nome de conexão do Cloud SQL para uso em aplicações."
  value       = google_sql_database_instance.postgres_instance.connection_name
}

output "db_public_ip_address" {
  description = "Endereço IP público do Cloud SQL (se habilitado e acessível)."
  value       = google_sql_database_instance.postgres_instance.public_ip_address
}

output "gcs_bucket_url" {
  description = "URL do bucket do Cloud Storage para arquivos estáticos."
  value       = "gs://${google_storage_bucket.static_files_bucket.name}"
}