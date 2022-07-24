# The cluster is a logical way to group a set of services to run
resource "aws_ecs_cluster" "ambro_cluster" {
    name = "ambro-cluster"
}

resource "aws_ecs_cluster_capacity_providers" "providers" {
    # By default, deploy using fargate provider, just 1 task

    cluster_name = aws_ecs_cluster.ambro_cluster.name

    capacity_providers = ["FARGATE", "FARGATE_SPOT"]

    default_capacity_provider_strategy {
        # Only one capacity provider in a capacity provider strategy can have a base defined.
        base              = 1    # At least 1 task should run by this capacity provider
        weight            = 100  # Percentage of tasks to deploy with this strategy 
        capacity_provider = "FARGATE_SPOT"  # By default, dont use fargate spot instances as a fallback may not be available to guarantee service availabity
  }
}

resource "aws_ecs_task_definition" "mytaskdef" {
    # A Task definition is a logical grouping of tasks (containers) which start and die together
    # For example a database should not be on the same task def as a server, but a metrics agent might
    # As it doesn't make sense to keep it alive if it can't observe anything
    family = "ambro-service"
    network_mode             = "awsvpc"     # Make aws manage networking to control who and how containers see each other https://tutorialsdojo.com/ecs-network-modes-comparison/
    requires_compatibilities = ["FARGATE"]  # This run is to be run on FARGATE
    task_role_arn = aws_iam_role.task_role.arn
    execution_role_arn = aws_iam_role.task_execution_role.arn

    # Fargate requires cpu and memory to be defined at the task level
    cpu       = 1024    # 0.25 virtual cpus
    memory    = 2048    # 2GB of RAM


    container_definitions = jsonencode([
        {
            name      = "flask-app"
            image     = "ambro17/twisted:production"

            essential = true  # If this task exits, all tasks of the service should exit transitively.
            portMappings = [
                {
                    containerPort = 80
                }
            ]


            logConfiguration = {
                logDriver = "awslogs"
                options = {
                    awslogs-region = "us-east-1"
                    awslogs-group = "${aws_cloudwatch_log_group.log_group.name}"
                    awslogs-stream-prefix = "ambro-service"  # Required to match the service to get the logs tab on the cluster
                    awslogs-create-group = "true"
                }
            }
        }
    ])
}

resource "aws_ecs_service" "service" {
    name                = "ambro-service"
    cluster             = aws_ecs_cluster.ambro_cluster.id
    task_definition     = aws_ecs_task_definition.mytaskdef.arn

    # The ECS Exec feature requires a task IAM role to grant containers the permissions needed for 
    # communication between the managed SSM agent (execute-command agent) and the SSM service.
    enable_execute_command = true  # Alllow entering to tasks (containers) inside the services

    desired_count          = 1

    network_configuration {
        security_groups  = [aws_security_group.secgroup.id]
        subnets = [aws_subnet.public.id]
        assign_public_ip = true
    }




    # Make Terraform not complain if the service has less or more instances due to scaling
    lifecycle {
        ignore_changes = [desired_count]
    }
}

resource "aws_security_group" "secgroup" {
    name   = "ambro-sg"
    description = "Allow TLS inbound traffic"
    vpc_id = aws_vpc.main.id
    # Allow HTTP Traffic
    ingress {
        protocol         = "tcp"
        from_port        = 80
        to_port          = 80
        cidr_blocks      = ["0.0.0.0/0"]
    }

    # Allow HTTPs Traffic
    ingress {
        protocol         = "tcp"
        from_port        = 443
        to_port          = 443
        cidr_blocks      = ["0.0.0.0/0"]
    }
 
    # Allow outbound to anywhere by any protocol
    egress {
        protocol         = "-1"  # Means every protocl
        from_port        = 0     # Forced by protocol == -1
        to_port          = 0     # Forced by protocol == -1
        cidr_blocks      = ["0.0.0.0/0"]  # Allow going everywhere
    }
}


resource "aws_cloudwatch_log_group" "log_group" {
  name = "${aws_ecs_cluster.ambro_cluster.name}-logs"
}