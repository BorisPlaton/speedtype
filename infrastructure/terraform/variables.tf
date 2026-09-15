variable "environment" {
  description = "Environment for which resources is being provisioned."
  type        = string

  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "Only dev, prod environments are allowed."
  }
}

variable "project_id" {
  description = "GCP project's id."
  type        = string
}
