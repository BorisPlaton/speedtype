locals {
  project_id  = var.project_id
  environment = var.environment

  sa = {
    name        = "zeus-${local.environment}-sa"
    permissions = toset([])
  }

  ksa = {
    name      = "zeus-${local.environment}-ksa"
    namespace = "zeus-${local.environment}"
    role      = "roles/iam.workloadIdentityUser"
  }

  secrets = {
    mongodb_username = {
      name   = "MONGODB_USERNAME_${local.environment}"
      length = 8
    }
    mongodb_password = {
      name                = "MONGODB_PASSWORD_${local.environment}"
      length              = 24
      add_special_symbols = true
    }
  }
}
