# test-gcp

I created this codebase as an opportunity to learn and demo Google Cloud Platform (GCP).  To learn the ecosystem, I figured I'd start with the basic building blocks of GCP like IAM, Storage, Pub/Sub, and Cloud Functions.  Also, I wanted to get my hands dirty _interacting_ with GCP from many angles, e.g. Terraform, `gcloud`, and the Python libraries.  To that end, I created a sample app and infrastructure, which I will describe below.

- First, I created [this](./infra/test_service_account) Terraform module to deploy a service account.

- Next, I _used_ that service account to deploy [this other](./infra/test_app) Terraform module (which comprises my 'app').

> **NOTE:**  In the first step, I deployed via my personal identity.  However, in the second step, I deployed _via the service account_ (i.e. all Terraform executions are subject to the service account's IAM permissions), because I wanted to simulate a hands-off CI/CD context.

> **NOTE:**  Currently, my 'app' is quite uninteresting.  It's just a Pub/Sub topic and pull subscription.  Eventually, I plan to string multiple components together as a learning exercise, e.g. Pub/Sub triggers a Cloud Function which then inserts a record into a BigQuery table.  Or something.  I just haven't gotten that far yet.

- Lastly, I created a Python [script](./scripts/test_pubsub.py) to test the app infra deployed above.



## Contents

- [Setup](#setup)
    - [Configure personal identity in gcloud](#configure-personal-identity-in-gcloud)
    - [Configure personal identity in non-gcloud tools](#configure-personal-identity-in-non-gcloud-tools)
    - [Deploy service account via Terraform](#deploy-service-account-via-terraform)
    - [Configure service account in gcloud](#configure-service-account-in-gcloud)
    - [Configure service account in non-gcloud tools](#configure-service-account-in-non-gcloud-tools)
    - [Deploy app via Terraform](#deploy-app-via-terraform)
- [References](#references)



## Setup

### Configure personal identity in gcloud

First, I installed `gcloud` and created a default configuration that accesses GCP via my personal identity:

```bash
gcloud init
gcloud auth login
```


### Configure personal identity in non-gcloud tools

In `gcloud`, access credentials are typically stored within [configurations](https://cloud.google.com/sdk/gcloud/reference/topic/configurations).  Unfortunately, non-`gcloud` tools (like Terraform and Python libraries) cannot use these configurations.  Instead, they require a _credential file_.  The [command](https://cloud.google.com/sdk/gcloud/reference/auth/application-default) below uses a browser pop-up to authenticate and fetch user credentials, which get stored locally.  If this credential file exists, non-`gcloud` tools can auto-detect it via the [ADC strategy](https://cloud.google.com/docs/authentication/application-default-credentials).

```bash
gcloud auth application-default login
```


### Deploy service account via Terraform

Next, use Terraform to deploy [`infra/test_service_account`](./infra/test_service_account).

```bash
cd infra/test_service_account
terraform init
terraform plan
terraform apply
```

> **NOTE:**  Above, I am using my personal identity to deploy the service account resources.  Terraform uses ADC strategy to auto-detect my personal user credentials at `~/AppData/Roaming/gcloud/application_default_credentials.json`.  If I delete or rename this file, Terraform stops working.


### Configure service account in gcloud

First, generate a service account key.

```bash
cd infra/test_service_account
ACCOUNT_ID="test-svc-account-1"
PROJECT_ID="curious-entropy-199817"
EMAIL="$ACCOUNT_ID@$PROJECT_ID.iam.gserviceaccount.com"
gcloud iam service-accounts keys create key.json --iam-account=$EMAIL
```

Next, create a new gcloud configuration that uses this key.

```bash
gcloud config configurations create test-svc-account-1
gcloud config configurations activate test-svc-account-1
gcloud auth activate-service-account --project=$PROJECT_ID --key-file=key.json
```

At this point, all `gcloud` commands will be executed by the service account (_not_ the personal identity).

Lastly, here are some useful commands:

```bash
# Inspect the active configuration.
gcloud config list
# View all configurations.
gcloud config configurations list
# Switch back to personal identity.
gcloud config configurations activate default
```


### Configure service account in non-gcloud tools

In Terraform, we can simply inject the service account keys into the [Google provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/provider_reference).

```tf
provider "google" {
  project     = "my-project"
  region      = "my-region"
  credentials = file("path/to/service_account_key.json")
}
```

Alternatively, we can set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable prior to calling any `terraform` commands.


### Deploy app via Terraform

To simulate an automated CI/CD context, we want to deploy our app via the service account (_not_ via our personal identity).  To do this, verify the [`credentials`](infra/test_app/terraform.tfvars#L2) variable points to the JSON key generated above.  Then we can run:

```bash
cd infra/test_app
terraform init
terraform plan
terraform apply
```



## References

- [Understanding Google Cloud IAM concepts with stick figures](https://towardsdatascience.com/google-cloud-iam-with-stick-figures-cd5ce19c142b)
