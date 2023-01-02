output "project_id" {
  value       = var.project_id
  description = "Google Cloud project ID."
}


output "topic_id" {
    value       = google_pubsub_topic.test_topic.id
    description = "Pub/Sub topic ID."
}


output "sub_id" {
    value       = google_pubsub_subscription.test_sub.id
    description = "Pub/Sub subscription ID."
}
