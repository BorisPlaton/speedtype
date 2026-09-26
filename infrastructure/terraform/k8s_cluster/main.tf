locals {
  pods_range_name     = "pods"
  services_range_name = "services"
}

resource "google_container_cluster" "this" {
  name             = "${var.cluster_name}-${var.cluster_environment}"
  enable_autopilot = true

  #trivy:ignore:AVD-GCP-0051
  resource_labels = {
    "environment" = var.cluster_environment,
    "application" = var.cluster_name
  }

  location = var.zone
  node_locations = [
    var.zone
  ]

  network    = google_compute_network.vpc.self_link
  subnetwork = google_compute_subnetwork.subnet.name

  ip_allocation_policy {
    cluster_secondary_range_name  = local.pods_range_name
    services_secondary_range_name = local.services_range_name
  }

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = true
  }

  cluster_autoscaling {
    auto_provisioning_defaults {
      service_account = google_service_account.gke_node_sa.email
    }
  }

  master_authorized_networks_config {}
}

resource "google_compute_network" "vpc" {
  name                    = "${var.cluster_name}-vpc-${var.cluster_environment}"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name                     = "${var.region}-${var.cluster_environment}"
  region                   = var.region
  network                  = google_compute_network.vpc.self_link
  ip_cidr_range            = "10.0.0.0/24"
  private_ip_google_access = true

  log_config {
    aggregation_interval = "INTERVAL_1_MIN"
    flow_sampling        = 0.5
    metadata             = "EXCLUDE_ALL_METADATA"
  }

  secondary_ip_range {
    range_name    = local.pods_range_name
    ip_cidr_range = "10.1.0.0/16"
  }

  secondary_ip_range {
    range_name    = local.services_range_name
    ip_cidr_range = "10.2.0.0/24"
  }
}

resource "google_service_account" "gke_node_sa" {
  account_id   = "${var.cluster_name}-${var.cluster_environment}-node-sa"
  display_name = "GKE node service account."
}

resource "google_project_iam_member" "gke_node_sa_role" {
  project = var.project_id
  role    = "roles/container.defaultNodeServiceAccount"
  member  = "serviceAccount:${google_service_account.gke_node_sa.email}"
}
