variable "project_id" {
  description = "GCP project's id."
  type        = string
}

variable "name" {
  description = "Cluster's name."
  type        = string
}

variable "region" {
  description = "Region to provision cluster resources."
  type        = string
}

variable "zone" {
  description = "Zone where zonal cluster will be created."
  type        = string
}

variable "environment" {
  description = "Cluster's environment."
  type        = string
}
