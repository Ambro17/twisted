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

## Improvements
- Add VPC endpoint to database

**Low Priority**
- Deploy with availability across two zones.
- Create private subnet?
- Move log name to data resource and reference it on ecs file instead of roles
- Parametrize terraform with variables
