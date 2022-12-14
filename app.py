#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.root import RootStack

app = cdk.App()

stack_name = app.node.try_get_context("stack_name")
vpcs = app.node.try_get_context("vpcs")

vpcs_count = len(vpcs)
if len(vpcs) != 2:
    raise Exception(f"Expected 2 vpcs in the context, found {vpcs_count}")

RootStack(app, stack_name, vpcs)

app.synth()