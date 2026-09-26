resource "google_project_service" "required_apis" {
  for_each = toset(local.apis.required)

  project            = local.project_id
  disable_on_destroy = local.apis.disable_on_destroy
  service            = each.value
}

resource "google_artifact_registry_repository" "this" {
  depends_on = [google_project_service.required_apis]

  location      = local.artifact_registry.location
  repository_id = local.artifact_registry.repository_id
  format        = local.artifact_registry.format
  description   = local.artifact_registry.description
}

module "k8s_cluster" {
  source     = "./k8s_cluster"
  depends_on = [google_project_service.required_apis]

  cluster_region      = local.k8s_cluster.region
  cluster_environment = local.environment
  cluster_zone        = local.k8s_cluster.zone
  cluster_name        = local.k8s_cluster.cluster_name
}

module "zeus" {
  source     = "./zeus"
  depends_on = [google_project_service.required_apis]

  zeus_environment = local.environment
  sa_name          = local.zeus.sa_name
  sa_permissions   = local.zeus.sa_permissions
  ksa_name         = local.zeus.ksa_name
  ksa_namespace    = local.zeus.ksa_namespace
}
