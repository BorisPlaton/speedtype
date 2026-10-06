resource "google_project_service" "required_apis" {
  for_each = toset(local.apis.required)

  project            = local.project_id
  disable_on_destroy = local.apis.disable_on_destroy
  service            = each.value
}

module "tf_remote_state" {
  source = "./tf_remote_state"

  region = local.region
}

module "workload_identity_pool" {
  source = "./workload_identity_pool"
}
