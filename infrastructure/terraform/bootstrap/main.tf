module "tf_remote_state" {
  source = "./tf_remote_state"

  region = local.region
}

module "github_integration" {
  source     = "./github_integration"
  depends_on = [module.tf_remote_state]

  tf_remote_state_bucket_name = module.tf_remote_state.bucket_name
}
