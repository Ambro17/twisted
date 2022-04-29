# Slack integrations

## Prerequisites
0. Install just, our task runner with
```
brew install just
1. Ensure you have the app secrets
```
cp env.sample .env
# Load your .env file as you prefer but expose the variables defined in it
# I use dotenv with an .envrc file with a single line: 'dotenv' that loads from .env and exports it  

# Check variables are available
just check_secrets_exist
```

## Setup
### With docker
```
just run
```
### Locally
0. Create a virtualenv with python3.10 with your preferred choice
1. Install dev and main dependencies (dev inherits from main so it will install all you need)
`just install`
2. `just start`
