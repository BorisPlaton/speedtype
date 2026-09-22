locals {
  zeus_name              = "zeus"
  cluster_name           = "speedtype"
  artifact_registry_name = "speedtype-images"
}

resource "google_artifact_registry_repository" "this" {
  location      = var.region
  repository_id = "${local.artifact_registry_name}-${var.env}"
  format        = "DOCKER"
  description   = "Artifact registry for storing docker images of speedtype services."
}

module "speedtype_cluster" {
  source = "./k8s_cluster"

  region     = var.region
  zone       = var.zone
  env        = var.env
  name       = local.cluster_name
  project_id = var.project_id
}

module "zeus_workload_sa" {
  source = "./workload_sa"

  name          = "${local.zeus_name}-${var.env}-sa"
  ksa_name      = "${local.zeus_name}-${var.env}-ksa"
  ksa_namespace = "${local.zeus_name}-${var.env}"
  permissions   = toset([])
  project_id    = var.project_id
}

module "speedtype_secrets" {
  source = "./secrets"

  env = var.env
}
