output "gha_workload_identity_provider" {
  value = google_iam_workload_identity_pool_provider.github.name
}

output "terraform_sa" {
  value = google_service_account.terraform_ci.email
}

output "push_image_sa" {
  value = google_service_account.terraform_ci.email
}
