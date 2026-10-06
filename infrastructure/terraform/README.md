# Speedtype Infrastructure

Speedtype was designed to run on Google Cloud Platform (GCP) with GKE cluster. All infrastructure was written
accordingly, using
Terraform and Kubernetes.

## GCP Infrastructure

Infrastructure resources, such as: GKE, VPC, Subnets, etc. as written using Terraform.

### Terraform remote state

First of all, you need to set up a Cloud Storage bucket for the Terraform remote state.

For this, `bootstrap/` exists. It is a module that sets up the bucket that will be used by the `speedtype/` module.

Before applying the `speedtype/` module on a fresh environment, set up the Terraform remote state bucket with the
following commands:

```bash
cd bootstrap
export TF_VAR_project_id="your GCP project id"
terraform init
terraform apply -auto-approve
```

### Speedtype infrastructure

Once the remote state is set up, you can run regular commands on the speedtype infrastructure using standard Terraform
commands.

`speedtype/` is the module where the actual speedtype infrastructure lives: K8s cluster, Artifact Registry, etc.

To run commands against speedtype's infrastructure, follow these steps:

```bash
cd speedtype
export TF_VAR_project_id="your GCP project id"
export TF_VAR_environment="infrastructure environment"
terraform init \
  -backend-config="bucket=tf-remote-state-${TF_VAR_project_id}" \
  -backend-config="prefix=envs/${TF_VAR_environment}"
terraform apply -auto-approve
```

1. `export TF_VAR_...` — sets up Terraform variables using environment variables.
2. `terraform init` — switches to the specific environment state, depending on what you've set `TF_VAR_environment` to:
   `dev` or `prod`.

## Speedtype K8s Cluster
