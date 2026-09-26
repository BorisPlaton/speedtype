locals {
  project_id = var.project_id
  region     = var.region
  zone       = var.zone

  tf_remote_state = {
    location                    = local.region
    name                        = "tf-remote-state-${local.project_id}"
    enable_versioning           = true
    uniform_bucket_level_access = true
  }
}
