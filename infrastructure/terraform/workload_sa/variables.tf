variable "name" {
  description = "Service account name."
  type        = string
}

variable "project_id" {
  description = "Project ID in which service account is being created."
  type        = string
}

variable "permissions" {
  description = "Set of permissions that are assigned to the service account."
  type        = set(string)
}

variable "ksa_name" {
  description = "Name of the Kubernetes service account to bind the GCP service account with."
  type        = string
}

variable "ksa_namespace" {
  description = "Namespace in which Kubernetes service account is being used."
  type        = string
}
