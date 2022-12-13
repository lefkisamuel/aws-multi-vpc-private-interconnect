
from constructs import Construct
from aws_cdk import (
    Stack,
)
from stacks.vpcs import VPCStack

class RootStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpcs:dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        VPCStack(self, f"{self.stack_name}VPC", vpcs)

