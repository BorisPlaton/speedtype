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

#############
## SECRETS ##
#############

resource "google_secret_manager_secret" "mongodb_username" {
  secret_id = local.secrets.mongodb_username.name

  replication {
    auto {}
  }
}

resource "random_string" "mongodb_username" {
  length = local.secrets.mongodb_username.length
}

resource "google_secret_manager_secret_version" "mongodb_username" {
  secret      = google_secret_manager_secret.mongodb_username.id
  secret_data = random_string.mongodb_username.result
}


resource "google_secret_manager_secret" "mongodb_password" {
  secret_id = local.secrets.mongodb_password.name

  replication {
    auto {}
  }
}

resource "random_password" "mongodb_password" {
  length  = local.secrets.mongodb_password.length
  special = local.secrets.mongodb_password.add_special_symbols
}

resource "google_secret_manager_secret_version" "mongodb_password" {
  secret      = google_secret_manager_secret.mongodb_password.id
  secret_data = random_password.mongodb_password.result
}
