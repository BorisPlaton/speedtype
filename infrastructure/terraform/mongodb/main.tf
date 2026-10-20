#############
## SECRETS ##
#############

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

#################
## PERMISSIONS ##
#################

resource "google_secret_manager_secret_iam_member" "eso_sa" {
  project   = local.project_id
  secret_id = local.secrets.mongodb_password.name
  role      = local.eso_sa.role
  member    = local.eso_sa.member
}
