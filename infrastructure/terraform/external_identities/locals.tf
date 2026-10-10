locals {
  project_id = var.project_id

  workload_identity_pool_name = "external-identities"

  github = {
    full_repository_name = "BorisPlaton/speedtype"
  }

  artifact_registry = {
    name     = var.artifact_registry_name
    location = var.artifact_registry_location
  }

  github_identity_pool = {
    provider_name       = "github-provider"
    issuer_uri          = "https://token.actions.githubusercontent.com"
    attribute_condition = "assertion.repository == '${local.github.full_repository_name}'"

    attribute_mapping = {
      "google.subject"       = "assertion.sub"
      "attribute.repository" = "assertion.repository"
    }
  }

  terraform_sa = {
    account_id  = "terraform-ci"
    member_role = "roles/iam.workloadIdentityUser"

    remote_state = {
      bucket_name = var.tf_remote_state_bucket_name
      role        = "roles/storage.objectUser"
    }

    sa_member_roles = [
      "roles/compute.networkAdmin",
      "roles/container.admin",
      "roles/artifactregistry.admin",
      "roles/iam.serviceAccountAdmin",
      "roles/resourcemanager.projectIamAdmin",
      "roles/secretmanager.admin",
    ]
  }

  push_image_sa = {
    member_role            = "roles/iam.workloadIdentityUser"
    artifact_registry_name = var.artifact_registry_name

    sa_member_roles = [
      "roles/artifactregistry.writer",
    ]
  }
}
