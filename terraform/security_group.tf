# Get default VPC
data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "bfsi_sg" {
  name        = "${var.project_name}-${var.environment}-sg"
  description = "Security Group for BFSI LCA EC2 Instance with Docker PostgreSQL"
  vpc_id      = data.aws_vpc.default.id

  # 1. SSH Access
  ingress {
    description = "SSH Access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  # 2. HTTP Web Access (Nginx Gateway & Let's Encrypt validation)
  ingress {
    description = "HTTP Inbound"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # 3. HTTPS Web Access (Mandatory for browser mic getUserMedia permissions over network)
  ingress {
    description = "HTTPS Secure Inbound"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # 4. Direct FastAPI Backend & WebRTC Signaling
  ingress {
    description = "FastAPI Backend & WebSocket Signaling"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # 5. PostgreSQL (Internal / Restricted to EC2 itself and VPC)
  ingress {
    description = "PostgreSQL Internal"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    self        = true
  }

  # All Outbound Traffic
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-sg"
  }
}

