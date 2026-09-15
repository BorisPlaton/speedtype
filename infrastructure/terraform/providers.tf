provider "google" {
  project = data.google_project.this.id
  region  = var.region
  zone    = var.zone
}
