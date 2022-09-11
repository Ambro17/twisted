# Slack integrations

## Prerequisites
0. Install [just](https://github.com/casey/just), our task runner with
```
brew install just
```
1. Install terraform cli

2. Fill the app secrets with the real values
```
cp .env.sample .env # And then replace by real values
```

2. Now load your .env file as you prefer but ensure the variables defined in it get exported into your shell. Personally i use direnv plus an `.envrc` file with `dotenv` as its content to load variables from .env

3. Check variables are available
```
just check_secrets_exist
```


## Setup
### With docker
```
just runit
```

### Locally
0. Create a virtualenv with python3.10 with your preferred choice
1. Install dev and main dependencies (dev inherits from main so it will install all you need)
```
just install
```
2. Run the server
```
just start
```

