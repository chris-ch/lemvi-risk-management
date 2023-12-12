variable "config" {
  description = "Function configuration section"
  type        = object({
    max_instance_count = number,
    available_memory = string,
    available_cpu = string,
    timeout = number
  })
  default = {
    max_instance_count = 1,
    available_memory = "256M",
    available_cpu = "0.333",
    timeout = 60
  }
}

variable "environment_variables" {
  type = map(string)
}

variable "function_storage_name" {
  description = "Function storage name"
  type = string
}

variable "prefix" {
  description = "Function prefix"
  type = string
}

variable "name" {
  description = "Function name"
  type = string
}

variable "entry_point" {
  type = string
  default = "main"
}

variable "region" {
  description = "Function location"
  type = string
}

variable "description" {
  description = "Function description"
  type = string
  default = ""
}

variable "path_functions" {
  description = "Path of functions source directories"
  type = string
}

variable "path_requirements" {
  type = string
}

variable "path_local_archive" {
  type = string
}

variable "runtime" {
  type = string
  default = "python312"
}

variable "path_helper_module" {
  type = string
}
