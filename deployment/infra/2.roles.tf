# Role asumed by containers/tasks
resource "aws_iam_role" "task_role" {
  name               = "ambro-task-role"

  # Allow ecs to assume this role
  assume_role_policy = data.aws_iam_policy_document.ecs_asume_policy.json
}

resource "aws_iam_policy" "task_policy" {
  # Allow containers to connect to ssm agent (ssh-like connections)
  # Also allow sending logs to cloudwatch
  name        = "ssm-and-logs-policy"
  description = "A test policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
       {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": [
                "arn:aws:secretsmanager:${var.region}:${var.account}:secret:twisted-app-secrets-*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "ssmmessages:CreateControlChannel",
                "ssmmessages:CreateDataChannel",
                "ssmmessages:OpenControlChannel",
                "ssmmessages:OpenDataChannel"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:DescribeLogGroups"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:DescribeLogStreams",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:${var.region}:${var.account}:log-group:${aws_ecs_cluster.ambro_cluster.name}-logs:*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "role_to_policy" {
  role       = aws_iam_role.task_role.name
  policy_arn = aws_iam_policy.task_policy.arn
}


# Role used in Cluster to start new tasks/containers. 
# Needs ECR pull permissions
resource "aws_iam_role" "task_execution_role" {
  name               = "ambro-task-execution-role"

  # Allow ecs to assume this role
  assume_role_policy = data.aws_iam_policy_document.ecs_asume_policy.json
}


# For deployments, we need to send logs too
resource "aws_iam_policy" "task_execution_policy" {
  name        = "logs-policy"
  description = "Send logs policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:DescribeLogGroups"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:DescribeLogStreams",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:${var.region}:${var.account}:log-group:${aws_ecs_cluster.ambro_cluster.name}-logs:*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "task_execution_policy" {
  role       = aws_iam_role.task_execution_role.name
  policy_arn = aws_iam_policy.task_execution_policy.arn
}

# Resource-based policy or trust policy or trust relationship that allows an iam role to be
# asumed by ECS service
# We could restrict who by specifying an extra account argument. Maybe later
data "aws_iam_policy_document" "ecs_asume_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

