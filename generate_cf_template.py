from troposphere import Template
from troposphere.s3 import Bucket, Private, PublicReadWrite, PublicRead


class GenerateCFTemplate:
    def __init__(self):
        self.template = Template()

    def add_s3_bucket(self, bucket_name: str, access: str):
        if access.lower() == "private":
            bucket_resource = Bucket(bucket_name, AccessControl=Private)
        elif access.lower() == "publicreadwrite":
            bucket_resource = Bucket(
                bucket_name, AccessControl=PublicReadWrite
            )
        elif access.lower() == "publicread":
            bucket_resource = Bucket(bucket_name, AccessControl=PublicRead)
        else:
            raise ValueError(f"Unknown AccessControl Value Entered - {access}")

        self.template.add_resource(bucket_resource)

    def to_yaml(self):
        print(self.template.to_yaml())
