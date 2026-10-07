resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = local.github_pool.name
}

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.name
  workload_identity_pool_provider_id = local.github_pool.provider_name

  attribute_mapping   = local.github_pool.attribute_mapping
  attribute_condition = local.github_pool.attribute_condition

  oidc {
    issuer_uri = local.github_pool.issuer_uri
  }
}

resource "google_service_account" "terraform_ci" {
  account_id = local.ci_sa.account_id
}

resource "google_service_account_iam_member" "github_binding" {
  service_account_id = google_service_account.terraform_ci.name
  role               = local.ci_sa.member_role
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/${local.github_repository}"
}

resource "google_project_iam_member" "terraform_ci_role" {
  for_each = toset(local.ci_sa.sa_roles)
  project  = local.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.terraform_ci.email}"
}
