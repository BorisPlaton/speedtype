output "speedtype_cluster_endpoint" {
  value       = module.k8s_cluster.cluster_endpoint
  description = "The IP address of speedtype's Kubernetes cluster master."
}
