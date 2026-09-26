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

variable "project_id" {
  description = "GCP project's id."
  type        = string
}
