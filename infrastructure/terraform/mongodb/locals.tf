locals {
  project_id  = var.project_id
  environment = var.environment

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

  eso_sa = {
    role   = "roles/secretmanager.secretAccessor"
    member = "principal://iam.googleapis.com/projects/${data.google_project.this.number}/locations/global/workloadIdentityPools/${local.project_id}.svc.id.goog/subject/ns/external-secrets/sa/external-secrets"
  }
}
