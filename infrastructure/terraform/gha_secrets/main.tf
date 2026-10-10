resource "github_actions_secret" "terraform_sa" {
  for_each = local.secrets

  repository      = local.repository_name
  secret_name     = each.key
  plaintext_value = each.value
}
