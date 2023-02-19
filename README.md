# Twisted app

## App
Python app of a slack integration to interact with external services.
This folder should be considered as an independent repo. It's only artifact is a docker image
`Python > Docker > Image`

### Main tasks
```
just app/install          # Install dependencies
just app/start            # Start bot locally
just app/run              # Start bot via docker
just app/updateimage      # Update docker image used in deploys
```


## Deployment
Terraform deployment of the python app in ECS service of AWS.
The dependency towards app is a single docker images. No imports are done between folders.
`App Image > Terraform > ECS Service`

### Prerequisites
- An s3 bucket called `twisted-terraform`
- A dynamodb table called `terraform-state` with a `LockId` index to store terraform remote state
- A secret in [Secret Manager](https://us-east-1.console.aws.amazon.com/secretsmanager/listsecrets?region=us-east-1)  called `twisted-app-secrets` with required secrets in `config.py`
- [Aws Session Manager plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html#install-plugin-linux) (Optional, if you want to connect to the container)
- Replace `account_id` variable in `5.variables.tf` with your active account

### Main tasks
```
just deployment/infra/init     # Initialize terraform with aws remote state.
just deployment/infra/apply    # Create infra
just deployment/infra/enter    # Enter container
just deployment/infra/destroy  # Destroy infra
```


## Release new version
```
just app/updateimage         # Build image with the latest changes and push it to the registry
just deployment/infra/apply  # Use the new image to deploy a new version of the app
```