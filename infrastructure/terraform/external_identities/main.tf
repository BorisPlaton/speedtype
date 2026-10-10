############################
## WORKLOAD IDENTITY POOL ##
############################

resource "google_iam_workload_identity_pool" "this" {
  workload_identity_pool_id = local.workload_identity_pool_name
}

########################
## GITHUB INTEGRATION ##
########################

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.this.workload_identity_pool_id
  workload_identity_pool_provider_id = local.github_identity_pool.provider_name

  attribute_mapping   = local.github_identity_pool.attribute_mapping
  attribute_condition = local.github_identity_pool.attribute_condition

  oidc {
    issuer_uri = local.github_identity_pool.issuer_uri
  }
}

##################
## TERRAFORM SA ##
##################

resource "google_service_account" "terraform_ci" {
  account_id = local.terraform_sa.account_id
}

resource "google_service_account_iam_member" "github_binding" {
  service_account_id = google_service_account.terraform_ci.name
  role               = local.terraform_sa.member_role
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.this.name}/attribute.repository/${local.github.full_repository_name}"
}

resource "google_project_iam_member" "terraform_ci_role" {
  for_each = toset(local.terraform_sa.sa_member_roles)
  project  = local.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.terraform_ci.email}"
}

resource "google_storage_bucket_iam_member" "allow_crud_on_remote_state" {
  bucket = local.terraform_sa.remote_state.bucket_name
  role   = local.terraform_sa.remote_state.role
  member = "serviceAccount:${google_service_account.terraform_ci.email}"
}

###################
## PUSH IMAGE SA ##
###################

resource "google_service_account" "push_image_sa" {
  account_id = local.terraform_sa.account_id
}

resource "google_service_account_iam_member" "push_image_sa_binding" {
  service_account_id = google_service_account.push_image_sa.name
  role               = local.push_image_sa.member_role
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.this.name}/attribute.repository/${local.github.full_repository_name}"
}

resource "google_artifact_registry_repository_iam_member" "ci_push" {
  for_each = toset(local.push_image_sa.sa_member_roles)

  project    = local.project_id
  location   = local.artifact_registry.location
  repository = local.artifact_registry.name
  role       = each.value
  member     = "serviceAccount:${google_service_account.push_image_sa.email}"
}
