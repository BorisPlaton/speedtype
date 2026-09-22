resource "random_password" "mongodb_password" {
  length  = 24
  special = true
}

resource "random_string" "mongodb_username" {
  length = 8
}

resource "google_secret_manager_secret" "mongodb_username" {
  secret_id = "MONGODB_USERNAME_${var.env}"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "mongodb_password" {
  secret_id = "MONGODB_PASSWORD_${var.env}"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "mongodb_username" {
  secret      = google_secret_manager_secret.mongodb_username.id
  secret_data = random_string.mongodb_username.result
}

resource "google_secret_manager_secret_version" "mongodb_password" {
  secret      = google_secret_manager_secret.mongodb_password.id
  secret_data = random_password.mongodb_password.result
}
