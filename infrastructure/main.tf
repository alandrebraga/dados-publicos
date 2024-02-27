terraform {
  required_version = ">= 1.0"
  backend "local" {}
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

resource "google_storage_bucket" "dados_publicos" {
  name     = "dl_${var.project}"
  location = var.region

  storage_class               = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  force_destroy = true
}

resource "google_bigquery_dataset" "staging" {
  dataset_id = var.bq_landing_dataset
  project    = var.project
  location   = var.region
}

resource "google_bigquery_dataset" "production" {
  dataset_id = var.bq_processed_dataset
  project    = var.project
  location   = var.region
}
