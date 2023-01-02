terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}


provider "google" {
  project = var.project_id
  region  = "us-east1"
}


# Enable required APIs.
resource "google_project_service" "iam_api" {
  for_each = toset([
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "pubsub.googleapis.com",
  ])
  project                    = var.project_id
  service                    = each.key
  disable_dependent_services = true
}


# Create a service account.
resource "google_service_account" "svc_account" {
  account_id  = "test-svc-account-1"
  description = "Test service account 1."
}


# Allow personal user to access service account.
resource "google_service_account_iam_member" "iam_personal_account_roles" {
  service_account_id = google_service_account.svc_account.name
  role               = "roles/iam.serviceAccountUser"
  member             = "user:${var.user_id}"
}


# Add roles to service account.
resource "google_project_iam_member" "iam_svc_account_roles" {
  for_each = toset([
    "roles/cloudfunctions.admin",
    "roles/pubsub.admin",
    "roles/storage.admin",
  ])
  role = each.key
  member = "serviceAccount:${google_service_account.svc_account.email}"
  project = var.project_id
}
