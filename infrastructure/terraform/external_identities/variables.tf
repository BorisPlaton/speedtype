variable "project_id" {
  description = "GCP project's id."
  type        = string
}

variable "tf_remote_state_bucket_name" {
  description = "Terraform remote state bucket's name."
  type        = string
}

variable "artifact_registry_name" {
  description = "Name of the artifact registry name for Docker images."
  type        = string
}

variable "artifact_registry_location" {
  description = "Location where artifact registry is being provisioned."
  type        = string
}
