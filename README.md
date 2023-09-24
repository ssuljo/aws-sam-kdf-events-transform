# AWS Lambda Cart Abandonment Detection Function

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- events_transform - Code for the application's Lambda function.
- template.yaml - A template that defines the application's AWS resources.

## Architecture Diagram
![aws-diagram](./images/aws-diagram.jpeg)
## Overview
This AWS Lambda function is designed to process cart events and determine if the carts are abandoned within an e-commerce system. Cart abandonment refers to the situation where a user adds products to their online shopping cart but leaves the website or application without completing the purchase. This Lambda function calculates the time elapsed since the event and checks if it exceeds a predefined threshold, indicating cart abandonment. It then calculates the total value of abandoned carts and adds this information to the event payload. The function is intended to be used in combination with Amazon Kinesis data streams.

## Functionality
- **Cart Abandonment Detection**: The function analyzes cart events and calculates whether each cart is abandoned based on the time elapsed since the event.
- **Cart Total Calculation**: If a cart is abandoned, the function calculates the total value of the cart by summing the product prices multiplied by their quantities.
- **Event Transformation**: The function transforms the input event records, adding information about cart abandonment and cart total.
- **Logging**: The function utilizes logging to provide visibility into the processing of cart events.


## Prerequisites
Before deploying and running this project, ensure you have the following prerequisites:
- **AWS Account**: You must have an AWS account to deploy and execute Lambda functions.
- **AWS CLI**: Install and configure the AWS Command Line Interface (CLI) to manage AWS resources and configure your credentials.
- **AWS SAM CLI**: Install the AWS Serverless Application Model (SAM) CLI to package and deploy your Lambda function.
- **Python 3.9**: Ensure you have Python 3.9 installed on your local development environment.

## Deployment

To build and deploy the Python Lambda function for the first time, follow these steps:

1. Clone this repository to your local machine.

2. Navigate to the project directory containing the `template.yaml` file.

3. Build the application using the AWS SAM CLI:

```bash
sam build
```

4. Deploy the application using the AWS SAM CLI:

```bash
sam deploy --guided
```

During deployment, you'll be prompted for configuration settings:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

## Usage
The AWS Lambda function will automatically process incoming cart events. It will calculate if each cart is abandoned and, if so, calculate the cart's total value. The results will be added to the event payload, and the transformed records will be available for further processing.

## Monitoring
You can monitor the AWS Lambda function's execution, view logs, and set up alerts using AWS CloudWatch.

## Error Handling
The Lambda function includes basic error handling to log errors when processing cart events. You can extend error handling and logging as needed to suit your specific use case.

## Cleanup
To delete the sample application, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
sam delete --stack-name sam-kdf-events-transform
```