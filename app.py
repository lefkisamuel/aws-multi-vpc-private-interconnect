#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.root import RootStack

app = cdk.App()

stack_name = app.node.try_get_context("stack_name")
vpcs = app.node.try_get_context("vpcs")

if len(vpcs) < 2:
    raise Exception("There must be at least 2 VPCs defined in the context.")

RootStack(app, stack_name, vpcs)

app.synth()