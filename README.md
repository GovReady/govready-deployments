# Install (All Cross Platform)
- `python3`

## Available Deployments Types
| Provider                       | Stable Implementation                                                             |
|--------------------------------|-------------------------------------------------------------------------|
| Amazon Web Service             | No                                                                      |
| Microsoft Azure                | No                                                                      |
| On Prem - Distributed          | No                                                                      |
| On Prem - Simple               | Yes                                                                     |

## Code Structure
Deployments are python modules that reside in `deployments`.  Each deployment module will have the following:
- `deploy.py` - Code to deploy 
- `undeploy.py` - Code to remove deployment
- `config-validator.json` - JSON config that validates the user provided config.  

## Run
#### Init
This will generate a skeleton JSON configuration file for the deployment you choose to use.  It will output `deployment.json` to be used for specified deployment.

Example: `python run.py init`

#### Deploy
The config JSON file will be validated against a deployments `deployments/<deployment_type>/config-validator.json`.  Make sure the provided configuration file has all the required keys and optional keys if you want to override the defaults.

| Arguments & Flags                                   | Description                                                             |
|-----------------------------------------------------|-------------------------------------------------------------------------|
| `--config <config-file>`                            | JSON formatted file required to deploy                                  |
| `--type <type>`                                     | (Optional) Skip prompt and provide deployment type                      |

Example: `python run.py deploy --type onprem_simple --config configuration.json`

Example Configuration - `configuration.json: `
```json
{
    "ADDRESS": "localhost:8000",
    "ADMINS": [
      {"username": "username", "email":"first.last@example.com", "password": "REPLACEME"}
    ],
    "DATABASE_CONNECTION_STRING": "",
    "EMAIL_DOMAIN": "",
    "EMAIL_HOST": "",
    "EMAIL_PORT": "",
    "EMAIL_PW": "",
    "EMAIL_USER": "",
    "GIT_URL": "",
    "MAILGUN_API_KEY": "",
    "MOUNT_FOLDER": "",
    "NGINX_CERT": "",
    "NGINX_KEY": "",
    "SECRET_KEY": "2h1_4t$j4ln6k#7k6x+ym@w2x&nomgoxuuw+p82&3mq=c!pyw)",
    "VERSION": ""
}
```


#### Remove Deployment
Tears down deployment provided. 

| Arguments & Flags                                   | Description                                                             |
|-----------------------------------------------------|-------------------------------------------------------------------------|
| `--type <type>`                                     | (Optional) Skip prompt and provide deployment type                      |
 
Example: `python run.py undeploy --type onprem_simple`


