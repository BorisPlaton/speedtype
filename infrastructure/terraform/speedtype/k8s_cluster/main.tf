#############
## CLUSTER ##
#############

#trivy:ignore:AVD-GCP-0051
#trivy:ignore:AVD-GCP-0061
resource "google_container_cluster" "this" {
  name     = "${local.cluster.name}-${local.cluster.environment}"
  location = local.cluster.zone

  resource_labels = {
    "environment" = local.cluster.environment,
    "application" = local.cluster.name
  }

  network    = google_compute_network.vpc.self_link
  subnetwork = google_compute_subnetwork.subnet.name

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = local.cluster.remove_default_node_pool
  initial_node_count       = 1

  workload_identity_config {
    workload_pool = "${local.project_id}.svc.id.goog"
  }

  network_policy {
    enabled = local.cluster.enable_network_policy
  }

  ip_allocation_policy {
    cluster_secondary_range_name  = local.cluster.pods_range_name
    services_secondary_range_name = local.cluster.services_range_name
  }

  private_cluster_config {
    enable_private_nodes    = local.cluster.private_nodes
    enable_private_endpoint = local.cluster.private_master
  }
}

#trivy:ignore:AVD-GCP-0048
resource "google_container_node_pool" "this" {
  cluster  = google_container_cluster.this.name
  location = local.cluster.zone

  node_config {
    image_type   = local.cluster.node.image_type
    machine_type = local.cluster.node.machine_type
    spot         = local.cluster.node.spot

    # Google recommends custom service accounts that have cloud-platform
    # scope and permissions granted via IAM Roles.
    service_account = google_service_account.gke_node_sa.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    boot_disk {
      size_gb   = local.cluster.node.disk_size_gb
      disk_type = local.cluster.node.disk_type
    }

    workload_metadata_config {
      mode = local.cluster.node.metadata_server_mode
    }
  }

  autoscaling {
    min_node_count = local.cluster.node.min_node_count
    max_node_count = local.cluster.node.node_count
  }

  upgrade_settings {
    max_surge       = local.cluster.node.upgrade_max_surge
    max_unavailable = local.cluster.node.upgrade_max_unavailable
  }

  management {
    auto_repair  = local.cluster.node.auto_repair
    auto_upgrade = local.cluster.node.auto_upgrade
  }
}

################
## NETWORKING ##
################

resource "google_compute_network" "vpc" {
  name                    = local.vpc.name
  auto_create_subnetworks = local.vpc.auto_create_subnetworks
}

resource "google_compute_subnetwork" "subnet" {
  name                     = local.subnet.name
  region                   = local.subnet.region
  network                  = google_compute_network.vpc.self_link
  ip_cidr_range            = local.subnet.ip_cidr_range
  private_ip_google_access = local.subnet.private_ip_google_access

  log_config {
    aggregation_interval = local.subnet.log_config.aggregation_interval
    flow_sampling        = local.subnet.log_config.flow_sampling
    metadata             = local.subnet.log_config.metadata
  }

  secondary_ip_range {
    range_name    = local.cluster.pods_range_name
    ip_cidr_range = local.subnet.secondary_ranges[0]
  }

  secondary_ip_range {
    range_name    = local.cluster.services_range_name
    ip_cidr_range = local.subnet.secondary_ranges[1]
  }
}

#####################
## SERVICE ACCOUNT ##
#####################

resource "google_service_account" "gke_node_sa" {
  account_id   = local.node_sa.account_id
  display_name = local.node_sa.display_name
}

resource "google_project_iam_member" "gke_node_sa_role" {
  project = local.project_id
  role    = local.node_sa.role
  member  = "serviceAccount:${google_service_account.gke_node_sa.email}"
}
