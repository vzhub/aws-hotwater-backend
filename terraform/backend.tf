terraform {
  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "VladHomeCloud"
    workspaces {
      name = "aws-hotwater-backend"
    }
  }
}