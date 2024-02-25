locals {
  data_lake_bucket = "airquality"
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
