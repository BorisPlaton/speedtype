locals {
  project_id  = var.project_id
  environment = var.environment
  region      = var.region
  zone        = var.zone

  tf_remote_state = {
    location                    = local.region
    name                        = "tf-remote-state"
    enable_versioning           = true
    uniform_bucket_level_access = true
  }

  zeus = {
    sa_name        = "zeus-${local.environment}-sa",
    sa_permissions = toset([])
    ksa_name       = "zeus-${local.environment}-ksa"
    ksa_namespace  = "zeus-${local.environment}"
  }

  k8s_cluster = {
    region       = local.region
    zone         = local.zone
    cluster_name = "speedtype"
  }

  artifact_registry = {
    location      = local.region
    repository_id = "speedtype-images-${local.environment}"
    format        = "DOCKER"
    description   = "Artifact registry for storing docker images of speedtype services."
  }

  apis = {
    required = [
      "iam.googleapis.com",
      "cloudresourcemanager.googleapis.com",
      "compute.googleapis.com",
      "container.googleapis.com",
      "artifactregistry.googleapis.com",
      "secretmanager.googleapis.com",
    ]
    disable_on_destroy = false
  }
}
