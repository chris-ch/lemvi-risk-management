variable org_id {
  type    = string
}

variable project_id {
  type = string
}

variable "region" {
  type    = string
  default = "us-east1"
}

variable "zone" {
  type    = string
  default = "us-east1-a"
}

variable "environment" {
  type    = string
  default = "test"
}
