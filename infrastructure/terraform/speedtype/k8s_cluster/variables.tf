variable "project_id" {
  description = "Project ID in which cluster is being created."
  type        = string
}

variable "cluster_name" {
  description = "Cluster's name."
  type        = string
}

variable "cluster_region" {
  description = "Region to provision resources."
  type        = string
}

variable "cluster_zone" {
  description = "Zone where zonal cluster will be created."
  type        = string
}

variable "cluster_environment" {
  description = "Cluster's environment."
  type        = string
}
