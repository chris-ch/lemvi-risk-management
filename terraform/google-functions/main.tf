

resource "google_storage_bucket" "bucket_functions_deployment" {
  name     = var.function_storage_name
  location = var.region
  uniform_bucket_level_access = true
}

data "archive_file" "function_archives" {
  type        = "zip"
  source {
    content  = file(var.path_helper_module)
    filename = reverse(split("/", var.path_helper_module))[0]
  }
  source {
    content  = file(var.path_requirements)
    filename = "requirements.txt"
  }
  source {
    content  = file("${var.path_functions}/${var.name}/${replace(var.name, "-", "_")}.py")
    filename = "main.py"
  }
  output_path = join("/", [var.path_local_archive, "${join("-", ["functions", var.prefix, var.name])}.zip"])
}

resource "google_storage_bucket_object" "object_functions" {
  name   = reverse(split("/", data.archive_file.function_archives.output_path))[0]
  bucket = google_storage_bucket.bucket_functions_deployment.name
  source = data.archive_file.function_archives.output_path
}

resource "google_cloudfunctions2_function" "function" {
  name        = join("-", [var.prefix, var.name])
  location    = var.region
  description = var.description

  build_config {
    runtime     = var.runtime
    entry_point = var.entry_point
    source {
      storage_source {
        bucket = google_storage_bucket.bucket_functions_deployment.name
        object = google_storage_bucket_object.object_functions.name
      }
    }
  }

  service_config {
      max_instance_count = var.config.max_instance_count
      available_memory   = var.config.available_memory
      available_cpu   = var.config.available_cpu
      timeout_seconds    = var.config.timeout
      environment_variables = var.environment_variables
  }
}
