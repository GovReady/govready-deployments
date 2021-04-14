## Dependencies (Install beforehand)
- `python3`
- See specific deployment `README.md` for their dependencies

## Available Deployments Types
| Deployment Type       | Stable | Link to Deployment                                    |
|-----------------------|--------|-------------------------------------------------------|
| On Premise            | ✔      | [Documentation](deployments/onprem/README.md) |
| On Premise - Distributed | ❌      | [Documentation](deployments/onprem_distributed/README.md) |
| Amazon Web Service    | ❌      | [Documentation](deployments/aws/README.md) |
| Microsoft Azure       | ❌      | [Documentation](deployments/azure/README.md) |
| Google Cloud Platform | ❌      | [Documentation](deployments/gcp/README.md) |

## Code Structure
Deployments are python modules that reside in `deployments`.  Each deployment module will have the following:
- `deploy.py` - Code to deploy 
- `undeploy.py` - Code to remove deployment
- `config-validator.json` - JSON config that validates the user provided config.  

## Run
#### Init
This will generate a skeleton JSON configuration file for the deployment you choose to use.  It will output `deployment.json` to be used for specified deployment.

Example: `python run.py init` or `python run.py init --type onprem`

#### Deploy
For a deployment to run, it must have the contents of `deployments/<deployment_type>/config-validator.json` satisfied.
To satisfy those requirements you can:
- Set Environment variables that match the keys from the `config-validator.json`
- Set values in the configuration file created via the `init`.

If both the configuration file and the environment variables are set, the configuration file takes precedence.

| Arguments & Flags                                   | Description                                                             |
|-----------------------------------------------------|-------------------------------------------------------------------------|
| `--config <config-file>`                            | JSON formatted file required to deploy                                  |
| `--type <type>`                                     | (Optional) Skip prompt and provide deployment type                      |

Example: `python run.py deploy --type onprem --config configuration.json`


#### Remove Deployment
Tears down deployment provided. 

| Arguments & Flags                                   | Description                                                             |
|-----------------------------------------------------|-------------------------------------------------------------------------|
| `--type <type>`                                     | (Optional) Skip prompt and provide deployment type                      |
 
Example: `python run.py undeploy --type onprem`


## Database Support
- PostgreSQL
- MySQL
