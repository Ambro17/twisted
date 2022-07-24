# ECS Playground
~~Trying to understand what ECS is~~
ECS is complex, really. But now we have a working version and i learned a lot about subnets, permissions, roles and general AWS complexity.


## Concepts
- An ECS cluster is a logical wrapper to manage infra resources and behaviour under load
- A Service is an independent set of processes that make something useful. Host a web page, run a cron, etc
- A Service runs Tasks which are instances of Task Definitions.
- A Task Definition is a docker image with steroids (cpu,mem constraints, logging config, etc)
- A Task is a container with steroids (basically extra config options of behaviour)

## Architecture
![Architecture Diagram](Arch.png?raw=true)

## Access via ssh to the container/task
```bash
aws ecs execute-command 
--cluster ambro-cluster 
--task id 
--container flask-app 
--interactive 
--command "bash"
```

## Improvements
- Review task image revision config. Should we redeploy if target didn't change?
- Dont use latest tag on image and use twisted tag
- Add VPC endpoint to database

**Low Priority**
- Setup and test autoscaling policies
- Deploy with availability across two zones.
- Create private subnet?
- Move log name to data resource and reference it on ecs file instead of roles
- Add task id to terraform output
- Parametrize terraform with variables
