import logging.config
import uuid

from config import config
from generate_cf_template import GenerateCFTemplate


uuid_str = str(uuid.uuid4()).upper()


def main():
    logger = logging.getLogger(__name__ + "." + uuid_str)
    logging.config.dictConfig(config["logging_dict"])

    logger.info("STARTING CLOUD FORMATION TEMPLATE GENEfRATING")
    cf_generator = GenerateCFTemplate()

    logger.info("GENERATING S3 BUCKET")
    cf_generator.add_s3_bucket(
        "jackDevelopment2",
        "jack-development2",
        "Private"
    )

    logger.info("GENERATING ECS FARGATE CLUSTER")
    cf_generator.add_ecs_fargate_cluster()

    logger.info("ADDING ECR REPOSITORY")
    cf_generator.add_ecr_repository(
        "adoptAPetScraper2",
        "adopt_a_pet_scraper2"
    )

    logger.info("GENERATING ECS TASK DEFINITION")
    cf_generator.add_ecs_task_definition(
        cpu="512",
        memory="1024",
        network_mode="awsvpc",
        port=4444,
        container_definitions=[
            {
                "name": "selenium_standalone-chrome",
                "image": "selenium/standalone-chrome:latest",
                "port_bool": True
            },
            {
                "name": "adopt_a_pet_scraper",
                "image": "623215716102.dkr.ecr.us-east-2.amazonaws.com/"
                         "adopt_a_pet_scraper:0.0.3-beta",
                "port_bool": False
            }
        ]
    )

    logger.info("GENERATING YAML FILE")
    cf_generator.to_yaml()


if __name__ == "__main__":
    main()
