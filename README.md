# Twisted app

## App
Python app of a slack integration to interact with external services.
This folder should be considered as an independent repo. It's only artifact is a docker image
`Python > Docker > Image`

## Deployment
Terraform deployment of the python app in ECS service of AWS.
The dependency towards app is a single docker images. No imports are done between folders.
`App Image > Terraform > ECS Service`