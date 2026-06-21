variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-2"
}

variable "api_key" {
  description = "Static API key value to validate against X-API-Key header"
  type        = string
}

variable "metric_namespace" {
  description = "CloudWatch metric namespace"
  type        = string
  default     = "HotWater"
}
