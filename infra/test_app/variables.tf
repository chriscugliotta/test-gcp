variable "project_id" {
  type        = string
  nullable    = false
  description = "Google Cloud project ID."
}

variable "credentials" {
  type        = string
  nullable    = false
  description = "Path to service account key file."
}
