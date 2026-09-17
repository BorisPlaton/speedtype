locals {
  zeus_name    = "zeus"
  cluster_name = "speedtype"
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
