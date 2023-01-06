terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}


provider "google" {
  project     = var.project_id
  region      = "us-east1"
  credentials = file(var.credentials)
}


# Create a Pub/Sub topic.
resource "google_pubsub_topic" "test_topic" {
  name = "test-topic-1"
}


# Create a Pub/Sub 'pull' subscription.
resource "google_pubsub_subscription" "test_sub" {
  name  = "test-sub-1"
  topic = google_pubsub_topic.test_topic.name
}


# Create a Storage bucket.
resource "google_storage_bucket" "name" {
  name = "${var.project_id}-test-bucket-1"
  location = "us-east1"
  force_destroy = true
  uniform_bucket_level_access = true
  public_access_prevention = "enforced"
}
