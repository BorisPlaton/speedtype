#trivy:ignore:AVD-GCP-0051
resource "google_container_cluster" "this" {
  name             = "${local.cluster.name}-${local.cluster.environment}"
  enable_autopilot = local.cluster.enable_autopilot

  resource_labels = {
    "environment" = local.cluster.environment,
    "application" = local.cluster.name
  }

  location = local.cluster.region

  network    = google_compute_network.vpc.self_link
  subnetwork = google_compute_subnetwork.subnet.name

  ip_allocation_policy {
    cluster_secondary_range_name  = local.cluster.pods_range_name
    services_secondary_range_name = local.cluster.services_range_name
  }

  private_cluster_config {
    enable_private_nodes    = local.cluster.private_nodes
    enable_private_endpoint = local.cluster.private_master
  }

  cluster_autoscaling {
    auto_provisioning_defaults {
      service_account = google_service_account.gke_node_sa.email
    }
  }

  master_authorized_networks_config {}
}

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

resource "google_service_account" "gke_node_sa" {
  account_id   = local.node_sa.account_id
  display_name = local.node_sa.display_name
}

resource "google_project_iam_member" "gke_node_sa_role" {
  project = local.project_id
  role    = local.node_sa.role
  member  = "serviceAccount:${google_service_account.gke_node_sa.email}"
}
