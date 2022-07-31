output "cluster_name" {
  value = aws_ecs_cluster.ambro_cluster.name
}

output "service_name" {
  value = aws_ecs_service.service.name
}

output "task_role_arn" {
    value = aws_iam_role.task_role.arn
}

output "service_link" {
    value = "https://us-east-1.console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/ambro-cluster/tasks"
}

output "cluster_logs" {
    value = "https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/${aws_ecs_cluster.ambro_cluster.name}-logs"
}
/*
output "ssh" {
    aws ecs execute-command 
    --cluster ambro-cluster 
    --task 4337b88a747548e182e479673ff7863d4 
    --container twisted-app 
    --interactive 
    --command "bash"
    value = "aws ecs execute-command --cluster ${cluster_name.value} --task ID --container NAME --interactive --command 'bash'"
}
# Link to cluster
# Public ip of task
*/