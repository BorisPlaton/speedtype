##############
## SA / KSA ##
##############

resource "google_service_account" "sa" {
  account_id   = local.zeus.sa_name
  display_name = local.zeus.sa_name
}

resource "google_project_iam_member" "this" {
  for_each = local.zeus.sa_permissions

  project = local.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_service_account_iam_member" "this" {
  service_account_id = google_service_account.sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${local.project_id}.svc.id.goog[${local.zeus.ksa_namespace}/${local.zeus.ksa_name}]"
}

#############
## SECRETS ##
#############

resource "google_secret_manager_secret" "mongodb_username" {
  secret_id = "MONGODB_USERNAME_${local.environment}"

  replication {
    auto {}
  }
}

resource "random_string" "mongodb_username" {
  length = 8
}

resource "google_secret_manager_secret_version" "mongodb_username" {
  secret      = google_secret_manager_secret.mongodb_username.id
  secret_data = random_string.mongodb_username.result
}


resource "google_secret_manager_secret" "mongodb_password" {
  secret_id = "MONGODB_PASSWORD_${local.environment}"

  replication {
    auto {}
  }
}

resource "random_password" "mongodb_password" {
  length  = 24
  special = true
}

resource "google_secret_manager_secret_version" "mongodb_password" {
  secret      = google_secret_manager_secret.mongodb_password.id
  secret_data = random_password.mongodb_password.result
}
