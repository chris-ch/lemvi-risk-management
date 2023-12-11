resource "random_integer" "google_project_suffix" {
  min = 1000
  max = 9999
}

locals {
  project_id = "${var.environment}-${var.project_name}-${random_integer.google_project_suffix.result}"
}

provider "google" {
  project     = local.project_id
  region      = var.region
  zone        = var.zone
}

resource "google_project" "lemvi_risk_management_platform" {
  name       = "Lemvi Risk Management Platform"
  project_id = local.project_id
}
