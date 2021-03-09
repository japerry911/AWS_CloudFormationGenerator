import logging.config
import uuid

from config import config
from generate_cf_template import GenerateCFTemplate


uuid_str = str(uuid.uuid4()).upper()


def main():
    logger = logging.getLogger(__name__ + "." + uuid_str)
    logging.config.dictConfig(config["logging_dict"])

    logger.info("STARTING CLOUD FORMATION TEMPLATE GENERATING")
    cf_generator = GenerateCFTemplate()

    logger.info("GENERATING S3 BUCKET")
    cf_generator.add_s3_bucket("jackDevelopment", "Private")

    logger.info("OUTPUTTING YAML FILE TEXT")
    cf_generator.to_yaml()


if __name__ == "__main__":
    main()
