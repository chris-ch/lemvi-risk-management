output "function_source" {
  value = data.archive_file.function_archives.output_path
}

output "function_uri" {
  value = google_cloudfunctions2_function.function.service_config[0].uri
}
