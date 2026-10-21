##############
## SA / KSA ##
##############

resource "google_service_account" "this" {
  account_id   = local.sa.name
  display_name = local.sa.name
}

resource "google_project_iam_member" "this" {
  for_each = local.sa.permissions

  project = local.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.this.email}"
}

resource "google_service_account_iam_member" "this" {
  service_account_id = google_service_account.this.name
  role               = local.ksa.role
  member             = "serviceAccount:${local.project_id}.svc.id.goog[${local.ksa.namespace}/${local.ksa.name}]"
}
