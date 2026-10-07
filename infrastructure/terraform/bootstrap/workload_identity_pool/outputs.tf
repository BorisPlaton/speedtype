output "github_workload_identity_provider" {
  value = google_iam_workload_identity_pool_provider.github.name
}

output "github_terraform_service_account_email" {
  value = google_service_account.terraform_ci.email
}
