from aws_cdk import (
    aws_ec2 as ec2,
    aws_ec2 as SecurityGroup,
    NestedStack,
)
from constructs import Construct

class VPCStack(NestedStack):
    vpcs_by_name: dict[str:ec2.Vpc] = {}
    def __init__(self, scope: Construct, id: str, vpcs: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        for vpc_name, vpc_details in vpcs.items():
            cidr = vpc_details["cidr"]
            max_azs = vpc_details["max_azs"]
            private_subnets_with_egress = vpc_details["private_subnets_with_egress"]
            nb_nat_gateways = vpc_details["nb_nat_gateways"]

            self.vpcs_by_name[vpc_name]=ec2.Vpc(self, vpc_name,
                ip_addresses=ec2.IpAddresses.cidr(cidr),
                vpc_name=vpc_name,
                max_azs=max_azs,
                nat_gateways= 0 if private_subnets_with_egress == False else nb_nat_gateways,
                subnet_configuration=[
                    ec2.SubnetConfiguration(
                        name="public",
                        subnet_type=ec2.SubnetType.PUBLIC,
                        cidr_mask=24
                    ),
                    ec2.SubnetConfiguration(
                        name="private",
                        subnet_type=ec2.SubnetType.PRIVATE_ISOLATED if private_subnets_with_egress == False else ec2.SubnetType.PRIVATE_WITH_EGRESS,
                        cidr_mask=24
                    )
                ]
            )

        #loop through all vpcs and create a security group that allows all traffic from all other vpcs
        for vpc_name, vpc in self.vpcs_by_name.items():
            vpc_security_group = ec2.SecurityGroup(self, f"{vpc_name}SecurityGroup", vpc=vpc, allow_all_outbound=True, security_group_name=f"{vpc_name}SecurityGroup")
            for other_vpc_name, other_vpc in self.vpcs_by_name.items():
                if other_vpc_name != vpc_name:
                    vpc_security_group.add_ingress_rule(ec2.Peer.ipv4(other_vpc.vpc_cidr_block), ec2.Port.all_traffic())

        