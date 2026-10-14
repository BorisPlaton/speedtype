output "cluster_endpoint_ip" {
  value       = google_container_cluster.this.endpoint
  description = "The IP address of this cluster's Kubernetes master."
}
