locals {
  project_id  = data.google_project.this.project_id
  environment = var.environment

  zeus = {
    sa_name        = "zeus-${local.environment}-sa"
    sa_permissions = toset([])
    ksa_name       = "zeus-${local.environment}-ksa"
    ksa_namespace  = "zeus-${local.environment}"
  }
}
