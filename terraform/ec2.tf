# Find latest Ubuntu 22.04 LTS AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Render user_data with templatefile() – native Terraform, no deprecated data source
locals {
  user_data_rendered = templatefile("${path.module}/user_data.sh", {
    postgres_user     = var.postgres_user
    postgres_password = var.postgres_password
    postgres_db       = var.postgres_db
    aws_region        = var.aws_region
  })
}

# EC2 Instance (t3.medium: 2 vCPU, 4GB RAM)
resource "aws_instance" "bfsi_server" {
  ami                  = data.aws_ami.ubuntu.id
  instance_type        = var.instance_type
  key_name             = var.key_name != "" ? var.key_name : null
  vpc_security_group_ids = [aws_security_group.bfsi_sg.id]
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  user_data = local.user_data_rendered

  root_block_device {
    volume_size           = var.volume_size
    volume_type           = "gp3"
    iops                  = 3000
    throughput            = 125
    delete_on_termination = true
    encrypted             = true

    tags = {
      Name = "${var.project_name}-root-ebs"
    }
  }

  tags = {
    Name = "${var.project_name}-ec2"
  }
}

# Elastic IP (Fixes public IP across restarts)
resource "aws_eip" "bfsi_eip" {
  instance = aws_instance.bfsi_server.id
  domain   = "vpc"

  tags = {
    Name = "${var.project_name}-eip"
  }
}

