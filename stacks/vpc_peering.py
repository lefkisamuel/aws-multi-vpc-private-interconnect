from aws_cdk import (
    aws_ec2 as ec2,
    NestedStack,
)
from constructs import Construct
import uuid


class VPCPeeringNestedStack(NestedStack):
    def __init__(self, scope: Construct, id: str, vpcs_by_name: dict[str:ec2.Vpc],private_subnets_with_egress_by_vpc_name:dict[str:bool], **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        # Create the vpc peering connection between the two vpcs
        for vpc_name, vpc in vpcs_by_name.items():
            for other_vpc_name, other_vpc in vpcs_by_name.items():
                if other_vpc_name == vpc_name:
                    continue
                pcx = ec2.CfnVPCPeeringConnection(self, f"{vpc_name}To{other_vpc_name}PeeringConnection",
                    vpc_id=vpc.vpc_id,
                    peer_vpc_id=other_vpc.vpc_id,
                    peer_owner_id=self.account,
                    peer_region=self.region
                ) 
                break
            break
        
        # Create the routes for the vpcs to talk to each other through the vpc peering connection
        for vpc_name, vpc in vpcs_by_name.items():
            for other_vpc_name, other_vpc in vpcs_by_name.items():
                if other_vpc_name == vpc_name:
                    continue

                private_subnets_with_egress = private_subnets_with_egress_by_vpc_name[vpc_name]
                selection = vpc.select_subnets(
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED if private_subnets_with_egress == False else ec2.SubnetType.PRIVATE_WITH_EGRESS
                )

                for subnet in selection.subnets:
                    ec2.CfnRoute(self, f"{vpc_name}To{other_vpc_name}Route{uuid.uuid4()}",
                        route_table_id=subnet.route_table.route_table_id,
                        destination_cidr_block=other_vpc.vpc_cidr_block,
                        vpc_peering_connection_id=pcx.attr_id
                    )

                