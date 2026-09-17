variable "region" {
  description = "Default region to provision resources."
  type        = string
  default     = "europe-central2"
}

variable "zone" {
  description = "Default region's zone to provision resources."
  type        = string
  default     = "europe-central2-a"
}

variable "env" {
  description = "Environment for which resources is being provisioned."
  type        = string

  validation {
    condition     = contains(["dev", "prod"], var.env)
    error_message = "Only dev, prod environments are allowed."
  }
}

variable "project_id" {
  description = "GCP project's id."
  type        = string
}
