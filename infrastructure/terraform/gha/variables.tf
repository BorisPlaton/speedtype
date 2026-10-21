variable "secrets" {
  type        = map(string)
  description = "List of secrets to store for GitHub Actions."
}

variable "variables" {
  type        = map(string)
  description = "List of variables to store for GitHub Actions."
}
