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
  zone    = "us-east1-a"
}


# Enable IAM API.
resource "google_project_service" "iam_api" {
  project                    = var.project_id
  service                    = "iam.googleapis.com"
  disable_dependent_services = true
}


# Enable IAM Service Account Credentials API.
resource "google_project_service" "iam_credentials_api" {
  project                    = var.project_id
  service                    = "iamcredentials.googleapis.com"
  disable_dependent_services = true
}


# Create a service account.
resource "google_service_account" "svc_account" {
  account_id  = "test-svc-account-1"
  description = "Test service account 1."
}


# Define IAM policies.
# TODO:  Apply principle of least privilege.
data "google_iam_policy" "iam_policies" {
  binding {
    role = "roles/iam.serviceAccountUser"

    members = [
      "user:chriscugliotta@gmail.com",
    ]
  }

  binding {
    role = "roles/owner"

    members = [
      "serviceAccount:${google_service_account.svc_account.email}",
    ]
  }
}


# Apply IAM policies to service account.
resource "google_service_account_iam_policy" "svc_account_policies" {
  service_account_id = google_service_account.svc_account.name
  policy_data        = data.google_iam_policy.iam_policies.policy_data
}
