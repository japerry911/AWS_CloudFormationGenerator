from time import sleep
from typing import Dict, List

from troposphere import Template, Ref
from troposphere.ecr import Repository
from troposphere.ecs import (
    ContainerDefinition,
    Cluster,
    PortMapping,
    TaskDefinition
)
from troposphere.iam import Role
from troposphere.s3 import Bucket, Private, PublicReadWrite, PublicRead


class GenerateCFTemplate:
    def __init__(self):
        self.template = Template()

    def add_s3_bucket(self, title: str, bucket_name: str, access: str):
        if access.lower() == "private":
            bucket_resource = Bucket(
                title,
                BucketName=bucket_name,
                AccessControl=Private
            )
        elif access.lower() == "publicreadwrite":
            bucket_resource = Bucket(
                title,
                BucketName=bucket_name,
                AccessControl=PublicReadWrite
            )
        elif access.lower() == "publicread":
            bucket_resource = Bucket(
                title,
                BucketName=bucket_name,
                AccessControl=PublicRead
            )
        else:
            raise ValueError(f"Unknown AccessControl Value Entered - {access}")

        self.template.add_resource(bucket_resource)

    def add_ecs_fargate_cluster(self):
        ecs_cluster = Cluster("Cluster")

        self.template.add_resource(ecs_cluster)

    def create_ecs_executor_role(self):
        role = Role(
            "ecsExecutorRole",
            ManagedPolicyArns=[
                "arn:aws:iam::aws:policy/service-role/"
                "AmazonECSTaskExecutionRolePolicy",
                "arn:aws:iam::aws:policy/AmazonS3FullAccess",
                "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
            ],
            AssumeRolePolicyDocument={"Statement": [{
                "Action": ["sts:AssumeRole"],
                "Effect": "Allow",
                "Principal": {"Service": ["ecs.amazonaws.com"]}
            }]}
        )

        self.template.add_resource(role)

    def add_ecs_task_definition(
            self,
            container_definitions: List[Dict],
            cpu: str = "256",
            memory: str = "512",
            network_mode: str = "awsvpc",
            port: int = 80
    ):
        container_definitions_list = list()

        self.create_ecs_executor_role()

        for cd in container_definitions:
            try:
                container_definitions_list.append(
                    ContainerDefinition(
                        Name=cd["name"],
                        Image=cd["image"],
                        Essential=True,
                        PortMappings=[PortMapping(ContainerPort=port)]
                    ) if cd["port_bool"] is True else
                    ContainerDefinition(
                        Name=cd["name"],
                        Image=cd["image"],
                        Essential=True,
                    )
                )
            except KeyError as exc:
                raise KeyError(
                    f"Missing Key in container definition(s) - {exc}"
                )

        task_definition = TaskDefinition(
            "TaskDefinition",
            RequiresCompatibilities=["FARGATE"],
            Cpu=cpu,
            Memory=memory,
            NetworkMode=network_mode,
            ContainerDefinitions=container_definitions_list,
            ExecutionRoleArn=Ref(Role("ecsExecutorRole"))
        )

        self.template.add_resource(task_definition)

    def add_ecr_repository(
            self,
            title: str,
            repo_name: str
    ):
        repo_to_add = Repository(
            title,
            RepositoryName=repo_name
        )

        self.template.add_resource(repo_to_add)

    def to_yaml(self):
        yaml = self.template.to_yaml()

        # added 1 second of sleep so that it does not print before logs output
        sleep(1)
        print(yaml)

        with open("./cloud_formation_template.yaml", "w") as write_file:
            write_file.write(yaml)
