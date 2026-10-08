locals {
  project_id = data.google_project.this.project_id

  github = {
    repository           = "speedtype"
    full_repository_name = "BorisPlaton/speedtype"

    secrets = {
      names = {
        gcp_project_id             = "GCP_PROJECT_ID"
        tf_remote_state_bucket     = "TERRAFORM_REMOTE_STATE_BUCKET"
        terraform_sa               = "TERRAFORM_SERVICE_ACCOUNT"
        workload_identity_provider = "WORKLOAD_IDENTITY_PROVIDER"
      }
      values = {
        gcp_project_id         = local.project_id
        tf_remote_state_bucket = "${local.terraform_sa.remote_state.bucket_name}-${local.project_id}"
      }
    }
  }

  github_identity_pool = {
    name                = "github-pool"
    provider_name       = "github-provider"
    issuer_uri          = "https://token.actions.githubusercontent.com"
    attribute_condition = "assertion.repository == '${local.github.full_repository_name}'"

    attribute_mapping = {
      "google.subject"       = "assertion.sub"
      "attribute.repository" = "assertion.repository"
    }
  }

  terraform_sa = {
    remote_state = {
      bucket_name = var.tf_remote_state_bucket_name
      role        = "roles/storage.objectUser"
    }
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
