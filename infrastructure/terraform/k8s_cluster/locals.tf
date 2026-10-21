locals {
  project_id = var.project_id
  region     = var.region

  cluster = {
    name                     = var.name
    environment              = var.environment
    zone                     = var.zone
    pods_range_name          = "pods"
    services_range_name      = "services"
    private_nodes            = true
    private_master           = false
    remove_default_node_pool = true
    enable_network_policy    = true
    deletion_protection      = false

    node = {
      node_count              = 2
      min_node_count          = 0
      machine_type            = "e2-standard-2"
      image_type              = "COS_CONTAINERD"
      spot                    = true
      disk_size_gb            = 35
      disk_type               = "pd-standard"
      auto_repair             = true
      auto_upgrade            = true
      upgrade_max_surge       = 1
      upgrade_max_unavailable = 0
      metadata_server_mode    = "GKE_METADATA"
    }

    workload_identity_config = {
      workload_pool = "${local.project_id}.svc.id.goog"
    }

    gateway_api_config = {
      channel = "CHANNEL_STANDARD"
    }
  }

  vpc = {
    auto_create_subnetworks = false
    name                    = "${local.cluster.name}-vpc-${local.cluster.environment}"
  }

  router = {
    name = "${local.vpc.name}-router"
  }

  nat = {
    name                               = "${local.vpc.name}-nat"
    nat_ip_allocate_option             = "AUTO_ONLY"
    source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

    log_config = {
      enable = true
      filter = "ERRORS_ONLY"
    }
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
