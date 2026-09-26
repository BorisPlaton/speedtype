output "k8s_cluster_endpoint_ip" {
  value       = module.k8s_cluster.cluster_endpoint_ip
  description = "The IP address of speedtype's Kubernetes cluster master."
}
