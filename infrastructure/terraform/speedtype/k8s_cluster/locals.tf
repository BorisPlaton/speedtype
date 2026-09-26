locals {
  project_id = var.project_id
  region     = var.region

  cluster = {
    name                = var.cluster_name
    environment         = var.cluster_environment
    region              = local.region
    enable_autopilot    = true
    pods_range_name     = "pods"
    services_range_name = "services"
    private_nodes       = true
    private_master      = true
  }

  vpc = {
    auto_create_subnetworks = false
    name                    = "${local.cluster.name}-vpc-${local.cluster.environment}"
  }

  subnet = {
    name                     = local.region
    region                   = local.region
    ip_cidr_range            = "10.0.0.0/24"
    private_ip_google_access = true
    secondary_ranges = [
      "10.1.0.0/16",
      "10.2.0.0/24",
    ]
    log_config = {
      aggregation_interval = "INTERVAL_1_MIN"
      flow_sampling        = 0.5
      metadata             = "EXCLUDE_ALL_METADATA"
    }
  }

  node_sa = {
    account_id   = "${local.cluster.name}-${local.cluster.environment}-node-sa"
    display_name = "GKE node service account."
    role         = "roles/container.defaultNodeServiceAccount"
  }
}
