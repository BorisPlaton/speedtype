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

  region      = local.k8s_cluster.region
  environment = local.environment
  zone        = local.k8s_cluster.zone
  name        = local.k8s_cluster.cluster_name
}

module "zeus" {
  source     = "./zeus"
  depends_on = [google_project_service.required_apis]

  environment = local.environment
}
