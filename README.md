# AWS Hotwater Backend - Terraform

This repository contains Terraform configuration and a Lambda handler that receives temperature metrics and pushes a custom CloudWatch metric.

## Provisioning with Terraform Cloud

1. Create a Terraform Cloud organization and workspace.
2. Configure the workspace with AWS credentials and any required variables:
   - `api_key`
   - `region`
3. Optionally add a backend block to `terraform/backend.tf`:

```hcl
terraform {
  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "YOUR_ORG"
    workspaces {
      name = "YOUR_WORKSPACE"
    }
  }
}
```

4. Authenticate with Terraform Cloud and initialize:

```bash
cd terraform
tfenv install # optional if using tfenv
terraform login
terraform init
```

5. If you prefer local variable files, create `terraform/terraform.tfvars` with:

```hcl
api_key = "your_static_api_key_here"
region  = "us-east-1"
```

6. Run Terraform from `terraform`:

```bash
terraform apply
```

## Usage

After `terraform apply`, Terraform outputs `api_endpoint`.

Send a POST request to `/metrics` with header `X-API-Key` and JSON body:

```json
{
  "device": "hotwater-tank",
  "temperature_c": 20.9375,
  "rssi": -65,
  "millis": 272139
}
```

Example curl:

```bash
curl -X POST "$API_ENDPOINT/metrics" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_static_api_key_here" \
  -d '{"device":"hotwater-tank","temperature_c":20.9375,"rssi":-65,"millis":272139}'
```
