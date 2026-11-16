variable "aws_region" {
  description = "AWS Region to deploy the EC2 instance"
  type        = string
  default     = "us-east-1" # N. Virginia – FinOps target region
}

variable "project_name" {
  description = "Project identifier"
  type        = string
  default     = "bfsi-ai-assist"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "poc"
}

variable "instance_type" {
  description = "EC2 Instance type (FinOps optimized: t3.medium provides 2 vCPU, 4GB RAM)"
  type        = string
  default     = "t3.medium"
}

variable "key_name" {
  description = "Name of existing AWS EC2 Key Pair for SSH access"
  type        = string
  default     = ""
}

variable "allowed_ssh_cidr" {
  description = "CIDR block permitted for SSH access"
  type        = string
  default     = "0.0.0.0/0"
}

variable "volume_size" {
  description = "Root EBS storage size in GB (gp3)"
  type        = number
  default     = 30
}

variable "postgres_password" {
  description = "Root password for Docker PostgreSQL database"
  type        = string
  default     = "bfsi_secure_pass_2025"
  sensitive   = true
}

variable "postgres_db" {
  description = "Database name"
  type        = string
  default     = "bfsi_db"
}

variable "postgres_user" {
  description = "Database username"
  type        = string
  default     = "postgres"
}

