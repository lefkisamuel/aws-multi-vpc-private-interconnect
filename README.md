# aws-multi-vpc-private-interconnecta
## Table of Contents:
- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation and Setup](#installation-and-setup)
  - [Usage](#usage)
    - [Configuration options](#configuration-options)
    - [Provisioned resources](#provisioned-resources)
    - [Deployment](#deployment)
- [Architecture](#architecture)
- [Clean-up](#clean-up)
- [License](#license)

## Overview
This project was designed to quickly create proof-of-concepts for applications that require communication between different private networks. This AWS Cloud Development Kit (CDK) application deploys two Amazon Virtual Private Clouds (VPCs) and connects them through a VPC peering connection, providing a basic private network that can be used as a foundation for more complex architectures.

## Getting Started
### Prerequisites
- An AWS account and credentials
- Node.js and the AWS CDK Toolkit installed
- Python 3.6 or later
- The Python package installer (pip) and virtual environment manager (virtualenv)

### Installation and Setup
1. Clone the repository to your local machine:
```
git clone https://github.com/lefkisamuel/aws-multi-vpc-private-interconnect
```
2. Navigate to the project's root directory:
```
cd aws-multi-vpc-private-interconnect
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Configure the VPCs by editing the `cdk.context.json` file at the root of the repository. For more information, see the [Usage](#Usage) section below.

### Usage
This application is implemented using the AWS CDK. In order to deploy the cloud resources, a context must be provided to the CDK application. Here is an example of how to configure and deploy the resources for this application. 

#### Configuration options
The `cdk.context.json` file, which is located at the root level of the repository, is used to provide configuration options to the CDK stack. An example of its usage is shown below:
```
{
    "stack_name":"VPCPeeringPoC",
    "vpcs":{
        "vpc1":{
            "cidr":"10.0.0.0/16",
            "max_azs":2,
            "nb_nat_gateways":1,
            "private_subnets_with_egress":true
        },
        "vpc2":{
            "cidr":"10.1.0.0/16",
            "max_azs":2,
            "nb_nat_gateways":1,
            "private_subnets_with_egress":true
        }
    }
}
```

The `stack_name` attribute must be specified to provide a name for the CloudFormation root stack. This value will be used to identify the stack in the AWS management console and in other AWS tools. 

The `vpcs` object contains configuration options for two Virtual Private Clouds (VPCs), named "vpc1" and "vpc2". It is important to note that the current implementation of this CDK project requires exactly two VPCs to be configured, and that these VPCs will be privately interconnected using a VPC peering connection. For each VPC, the following options are provided:

- `cidr`: The CIDR block for the VPC.
- `max_azs`: The maximum number of Availability Zones (AZs) to use for the VPC.
- `nb_nat_gateways`: The number of NAT gateways to create for the VPC.
- `private_subnets_with_egress`: A boolean value indicating whether private subnets in the VPC should have internet egress enabled. _Note that if you set the private_subnets_with_egress option to False, the application will not create any NAT gateways for the VPCs_

These configuration options can be used to customize the behavior of the CDK stack when it is deployed. For example, the VPC CIDR blocks and the number of NAT gateways can be adjusted to fit the needs of the specific environment in which the stack is being deployed.

#### Provisioned resources
The following table lists the provisioned resources and their descriptions:

| Resource Type | Description | 
|----------|----------|
| VPCs   | Two VPCs are deployed. |
| Public Subnets | The number of public subnets is determined by the value of the max_azs attribute. For instance, if this is set to 2, then two public subnets will be provisioned. |
| Private Subnets | The number of private subnets is the same as the number of public subnets. |
|Internet Gateways| One internet gateway is deployed per VPC.|
| NAT Gateways   | The number of NAT gateways depends on the configuration of the context. By default, one NAT gateway per VPC is provisioned. However, if private_subnets_with_egress is set to False, then no NAT gateways will be deployed. |
| VPC Peering Connection | A VPC Peering Connection between the two VPCs is provisioned with auto-accept enabled.| 
| Routes | Routes are configured to allow traffic from the private subnets of a VPC to the other VPC's CIDR. |
|Security Groups| A security group is created for each VPC to allow all traffic between the two VPCs.|


#### Deployment
To deploy the configured cloud resources, run the following command:
```
cdk deploy
```

## Architecture
The application deploys two VPCs and connects them using a VPC peering connection. The following diagram illustrates the architecture:
![Architecture Diagram](.attachments/diagram.svg)

## Clean-up
To clean up the stacks, you can use the cdk destroy command as shown below:
```
cdk destroy
```
This command will delete all resources that were created by the stacks. Failing to delete resources such as NAT Gateways can result in ongoing charges for their usage. 

## License
The project is licensed under the MIT license, which allows users to use, modify, and distribute the project's code and documentation for any purpose, as long as the original copyright and license notice is included.