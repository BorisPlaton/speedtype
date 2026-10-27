locals {
  project_id  = var.project_id
  environment = var.environment

  sa = {
    name = "zeus-${local.environment}-sa"
    permissions = toset([
      "roles/secretmanager.secretAccessor",
    ])
  }

  ksa = {
    name      = "zeus-${local.environment}-ksa"
    namespace = "zeus-${local.environment}"
    role      = "roles/iam.workloadIdentityUser"
  }
}
