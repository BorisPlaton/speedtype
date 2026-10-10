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

module "tf_remote_state" {
  source     = "./tf_remote_state"
  depends_on = [google_project_service.required_apis]

  project_id = local.project_id
  region     = local.region
}

module "external_identities" {
  source     = "./external_identities"
  depends_on = [module.tf_remote_state]

  project_id                  = local.project_id
  artifact_registry_name      = google_artifact_registry_repository.this.name
  artifact_registry_location  = local.artifact_registry.location
  tf_remote_state_bucket_name = module.tf_remote_state.bucket_name
}

module "k8s_cluster" {
  source     = "./k8s_cluster"
  depends_on = [google_project_service.required_apis]

  project_id  = local.project_id
  region      = local.k8s_cluster.region
  environment = local.environment
  zone        = local.k8s_cluster.zone
  name        = local.k8s_cluster.cluster_name
}

module "zeus" {
  source     = "./zeus"
  depends_on = [google_project_service.required_apis]

  project_id  = local.project_id
  environment = local.environment
}

module "gha_secrets" {
  source = "./gha_secrets"
  depends_on = [
    module.external_identities,
    module.tf_remote_state
  ]

  secrets = {
    GCP_PROJECT_ID                 = local.project_id
    TERRAFORM_REMOTE_STATE_BUCKET  = module.tf_remote_state.bucket_name
    GHA_WORKLOAD_IDENTITY_PROVIDER = module.external_identities.gha_workload_identity_provider
    TERRAFORM_SERVICE_ACCOUNT      = module.external_identities.terraform_sa
    PUSH_IMAGE_SERVICE_ACCOUNT     = module.external_identities.push_image_sa
  }
}
