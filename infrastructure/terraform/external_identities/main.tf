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

############################
## GITHUB ACTIONS SECRETS ##
############################

resource "github_actions_secret" "terraform_sa" {
  repository      = local.github.repository
  secret_name     = local.github.secrets.names.terraform_sa
  plaintext_value = google_service_account.terraform_ci.email
}

resource "github_actions_secret" "workload_identity_provider" {
  repository      = local.github.repository
  secret_name     = local.github.secrets.names.workload_identity_provider
  plaintext_value = google_iam_workload_identity_pool_provider.github.name
}

resource "github_actions_secret" "gcp_project_id" {
  repository      = local.github.repository
  secret_name     = local.github.secrets.names.gcp_project_id
  plaintext_value = local.github.secrets.values.gcp_project_id
}

resource "github_actions_secret" "tf_remote_state_bucket" {
  repository      = local.github.repository
  secret_name     = local.github.secrets.names.tf_remote_state_bucket
  plaintext_value = local.github.secrets.values.tf_remote_state_bucket
}
