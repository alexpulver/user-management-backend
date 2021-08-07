# Example project for working with AWS CDK, AWS SAM and AWS Chalice
This project shows how AWS CDK and AWS Chalice can be used together to build 
a component. AWS CDK is used to build the broader infrastructure, while using  
AWS Chalice as developer-friendly Python serverless microframework.

The project implements a *user management backend* component that uses 
Amazon API Gateway, AWS Lambda and Amazon DynamoDB to provide basic 
CRUD operations for managing users. The project also includes a continuous 
delivery pipeline.

## Create development environment
See [Getting Started With the AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
for additional details and prerequisites

### Clone the code
```bash
git clone -b future https://github.com/alexpulver/aws-cdk-sam-chalice
cd aws-cdk-sam-chalice
```

### Create Python virtual environment and install the dependencies
```bash
python3.7 -m venv .venv
source .venv/bin/activate
# [Optional] Needed to upgrade dependencies and cleanup unused packages
pip install pip-tools==6.1.0
./scripts/install-deps.sh
./scripts/run-tests.sh
```

### [Optional] Upgrade AWS CDK Toolkit version
**Note:** If you are planning to upgrade dependencies, first push the upgraded AWS CDK Toolkit version.
See [(pipelines): Fail synth if pinned CDK CLI version is older than CDK library version](https://github.com/aws/aws-cdk/issues/15519) 
for more details.

```bash
vi package.json  # Update "aws-cdk" package version
./scripts/install-deps.sh
./scripts/run-tests.sh
```

### [Optional] Upgrade dependencies (ordered by constraints)
Consider [AWS CDK Toolkit (CLI)](https://docs.aws.amazon.com/cdk/latest/guide/reference.html#versioning) compatibility 
when upgrading AWS CDK packages version.

```bash
pip-compile --upgrade api/runtime/requirements.in
pip-compile --upgrade requirements.in
pip-compile --upgrade requirements-dev.in
./scripts/install-deps.sh
# [Optional] Cleanup unused packages
pip-sync api/runtime/requirements.txt requirements.txt requirements-dev.txt
./scripts/run-tests.sh
```

## Deploy the component to development environment
The `UserManagementBackend-Dev` stage uses your default AWS account and region.
It consists of two stacks - stateful (database) and stateless (API and monitoring) 

```bash
npx cdk deploy "UserManagementBackend-Dev/*"
```

Example outputs for `npx cdk deploy "UserManagementBackend-Dev/*"`:
```text
 ✅  UserManagementBackendDevStateful7B33C11B (UserManagementBackend-Dev-Stateful)

Outputs:
UserManagementBackendDevStateful7B33C11B.ExportsOutputFnGetAttDatabaseTableF104A135ArnDAC15A6A = arn:aws:dynamodb:eu-west-1:807650736403:table/UserManagementBackend-Dev-Stateful-DatabaseTableF104A135-1LVXRPCPOKVZQ
UserManagementBackendDevStateful7B33C11B.ExportsOutputRefDatabaseTableF104A1356B7D7D8A = UserManagementBackend-Dev-Stateful-DatabaseTableF104A135-1LVXRPCPOKVZQ
```
```text
 ✅  UserManagementBackendDevStateless0E5B7E4B (UserManagementBackend-Dev-Stateless)

Outputs:
UserManagementBackendDevStateless0E5B7E4B.APIHandlerArn = arn:aws:lambda:eu-west-1:807650736403:function:UserManagementBackend-Dev-Stateless-APIHandler-PJjw0Jn7Waq0
UserManagementBackendDevStateless0E5B7E4B.APIHandlerName = UserManagementBackend-Dev-Stateless-APIHandler-PJjw0Jn7Waq0
UserManagementBackendDevStateless0E5B7E4B.EndpointURL = https://zx5s6bum21.execute-api.eu-west-1.amazonaws.com/v1/
UserManagementBackendDevStateless0E5B7E4B.RestAPIId = zx5s6bum21
```

## Deploy the pipeline
**Note:** The pipeline will deploy continuous build for pull requests

**Prerequisites**
- Fork the repository
- Create AWS CodeStar Connections [connection](https://docs.aws.amazon.com/dtconsole/latest/userguide/welcome-connections.html)
  for the pipeline
- Authorize AWS CodeBuild access for the continuous build
  - Start creating a new project manually
  - Select GitHub as Source provider
  - Choose **Connect using OAuth** (unless already connected using OAuth)
  - Authorize access and cancel the project creation
- Update the values in [constants.py](constants.py)

```bash
npx cdk deploy UserManagementBackend-Pipeline
```

## Delete all stacks
**Do not forget to delete the stacks to avoid unexpected charges**
```bash
npx cdk destroy "UserManagementBackend-Dev/*"
npx cdk destroy UserManagementBackend-Pipeline
npx cdk destroy "UserManagementBackend-Pipeline/UserManagementBackend-Prod/*"
```

## Testing the web API
Below are examples that show the available resources and how to use them:
```bash
curl \
    -H "Content-Type: application/json" \
    -X POST \
    -d '{"username":"john", "email":"john@example.com"}' \
    https://API_ID.execute-api.REGION.amazonaws.com/v1/users

curl \
    -H "Content-Type: application/json" \
    -X GET \
    https://API_ID.execute-api.REGION.amazonaws.com/v1/users/john

curl \
    -H "Content-Type: application/json" \
    -X PUT \
    -d '{"country":"US", "state":"WA"}' \
    https://API_ID.execute-api.REGION.amazonaws.com/v1/users/john

curl \
    -H "Content-Type: application/json" \
    -X DELETE \
    https://API_ID.execute-api.REGION.amazonaws.com/v1/users/john
```
