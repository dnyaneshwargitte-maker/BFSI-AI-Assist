output "ec2_public_ip" {
  description = "Elastic Public IP address of the EC2 instance"
  value       = aws_eip.bfsi_eip.public_ip
}

output "ec2_instance_id" {
  description = "EC2 Instance ID"
  value       = aws_instance.bfsi_server.id
}

output "customer_portal_url" {
  description = "URL for Policyholder Customer Self-Service Portal"
  value       = "http://${aws_eip.bfsi_eip.public_ip}/customer"
}

output "agent_portal_url" {
  description = "URL for Real-Time Agent Assist CRM Workbench"
  value       = "http://${aws_eip.bfsi_eip.public_ip}/agent"
}

output "gateway_portal_url" {
  description = "URL for Main Landing Gateway"
  value       = "http://${aws_eip.bfsi_eip.public_ip}/"
}

output "ssh_command" {
  description = "Command to connect via SSH"
  value       = "ssh -i <your-key.pem> ubuntu@${aws_eip.bfsi_eip.public_ip}"
}

output "docker_postgres_info" {
  description = "PostgreSQL Docker deployment info"
  value = {
    container = "bfsi_postgres"
    port      = 5432
    database  = var.postgres_db
    user      = var.postgres_user
  }
}

