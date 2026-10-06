locals {
  project_id = data.google_project.this.project_id

  tf_remote_state = {
    location                    = var.region
    name                        = "tf-remote-state-${local.project_id}"
    enable_versioning           = true
    uniform_bucket_level_access = true
  }
}
