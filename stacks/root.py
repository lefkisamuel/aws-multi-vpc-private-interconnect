
from constructs import Construct
from aws_cdk import (
    Stack,
)
from stacks.vpcs import VPCNestedStack
from stacks.vpc_peering import VPCPeeringNestedStack

class RootStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpcs:dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_nested_stack = VPCNestedStack(self, f"{self.stack_name}VPC", vpcs)
        VPCPeeringNestedStack(self, f"{self.stack_name}VPCPeering", vpc_nested_stack.vpcs_by_name, vpc_nested_stack.private_subnets_with_egress_by_vpc_name)