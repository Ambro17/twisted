# Commented until the app is ready to read secret via an iam permission
#
# resource "aws_secretsmanager_secret" "app_config" {
#     description = "Application configuration secrets"
#     name = "twisted-app-secrets"
# }