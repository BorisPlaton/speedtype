#trivy:ignore:AVD-GCP-0066
#trivy:ignore:AVD-GCP-0077
resource "google_storage_bucket" "tf_remote_state" {
  uniform_bucket_level_access = local.tf_remote_state.uniform_bucket_level_access
  name                        = local.tf_remote_state.name
  location                    = local.tf_remote_state.location

  versioning {
    enabled = local.tf_remote_state.enable_versioning
  }
}
