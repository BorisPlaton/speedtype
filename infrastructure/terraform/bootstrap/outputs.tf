output "github_terraform_service_account_email" {
  value = module.workload_identity_pool.github_terraform_service_account_email
}

output "github_workload_identity_provider" {
  value = module.workload_identity_pool.github_workload_identity_provider
}
