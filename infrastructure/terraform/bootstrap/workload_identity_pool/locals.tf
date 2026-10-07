locals {
  github_repository = "BorisPlaton/speedtype"
  project_id        = data.google_project.this.project_id

  github_pool = {
    name                = "github-pool"
    provider_name       = "github-provider"
    issuer_uri          = "https://token.actions.githubusercontent.com"
    attribute_condition = "assertion.repository == '${local.github_repository}'"

    attribute_mapping = {
      "google.subject"       = "assertion.sub"
      "attribute.repository" = "assertion.repository"
    }
  }

  ci_sa = {
    account_id  = "terraform-ci"
    member_role = "roles/iam.workloadIdentityUser"

    sa_member_roles = [
      "roles/compute.networkAdmin",
      "roles/container.admin",
      "roles/artifactregistry.admin",
      "roles/iam.serviceAccountAdmin",
      "roles/resourcemanager.projectIamAdmin",
      "roles/secretmanager.admin",
    ]
  }
}
