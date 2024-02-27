locals {
  data_lake_bucket = "dl"
}

variable "project" {
  description = "your project id"
  type        = string
  default     = "educacao-superior-415319"
}

variable "region" {
  description = "Region for GCP resources"
  default     = "us-east1"
  type        = string
}

variable "storage_class" {
  description = "storage class type for bucket"
  default     = "STANDARD"
}

variable "bq_landing_dataset" {
  description = "BigQuery dataset with raw data"
  type        = string
  default     = "raw_dados_publicos"
}

variable "bq_processed_dataset" {
  description = "BigQuery dataset with production data"
  type        = string
  default     = "processed_dados_publicos"
}
