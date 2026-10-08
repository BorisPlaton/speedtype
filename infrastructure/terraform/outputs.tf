output "k8s_cluster_endpoint_ip" {
  value       = module.k8s_cluster.cluster_endpoint_ip
  description = "The IP address of speedtype's Kubernetes cluster master."
}

output "artifact_registry_name" {
  value       = google_artifact_registry_repository.this.registry_uri
  description = "The IP address of speedtype's Kubernetes cluster master."
}
