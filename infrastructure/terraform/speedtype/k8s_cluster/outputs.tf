output "cluster_endpoint" {
  value       = google_container_cluster.this.endpoint
  description = "The IP address of this cluster's Kubernetes master."
}
