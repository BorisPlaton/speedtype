output "name" {
  value       = google_container_cluster.this.name
  description = "The name of the cluster."
}

output "location" {
  value       = google_container_cluster.this.location
  description = "The location of the cluster."
}
