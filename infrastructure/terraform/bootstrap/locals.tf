locals {
  project_id = var.project_id
  region     = "europe-central2"
  zone       = "europe-central2-a"

  apis = {
    required = [
      "iam.googleapis.com",
    ]
    disable_on_destroy = false
  }
}
