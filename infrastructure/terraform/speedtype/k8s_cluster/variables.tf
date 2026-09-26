variable "cluster_name" {
  description = "Cluster's name."
  type        = string
}

variable "project_id" {
  description = "Project ID in which cluster is being created."
  type        = string
}

variable "region" {
  description = "Region to provision cluster resources."
  type        = string
}

variable "cluster_environment" {
  description = "Cluster's environment."
  type        = string
}
