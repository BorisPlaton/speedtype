resource "google_service_account" "sa" {
  account_id   = var.name
  display_name = var.name
}

resource "google_project_iam_member" "this" {
  for_each = var.permissions

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_service_account_iam_member" "this" {
  service_account_id = google_service_account.sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = var.ksa_name
}
