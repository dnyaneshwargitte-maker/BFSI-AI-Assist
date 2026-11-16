# IAM Role for EC2 Instance to securely access Amazon Bedrock Claude 3.5 without hardcoded API keys
resource "aws_iam_role" "ec2_bedrock_role" {
  name = "${var.project_name}-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Policy granting Amazon Bedrock Model Invocation (Claude 3.5 Sonnet)
resource "aws_iam_policy" "bedrock_access_policy" {
  name        = "${var.project_name}-bedrock-policy"
  description = "Allows EC2 instance to invoke Amazon Bedrock Foundation Models"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream",
          "bedrock:ListFoundationModels"
        ]
        Resource = "*"
      }
    ]
  })
}

# Attach Bedrock Policy
resource "aws_iam_role_policy_attachment" "attach_bedrock" {
  role       = aws_iam_role.ec2_bedrock_role.name
  policy_arn = aws_iam_policy.bedrock_access_policy.arn
}

# Attach AWS Systems Manager (SSM) Policy for secure terminal access without SSH key if needed
resource "aws_iam_role_policy_attachment" "attach_ssm" {
  role       = aws_iam_role.ec2_bedrock_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Instance Profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.project_name}-instance-profile"
  role = aws_iam_role.ec2_bedrock_role.name
}

