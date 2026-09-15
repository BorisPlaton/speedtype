resource "github_actions_secret" "this" {
  for_each = local.secrets

  repository      = local.repository_name
  secret_name     = each.key
  plaintext_value = each.value
}

resource "github_actions_variable" "this" {
  for_each = local.variables

  repository    = local.repository_name
  variable_name = each.key
  value         = each.value
}
