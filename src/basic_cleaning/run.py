import argparse
import logging
import os
from typing import Any

import pandas as pd
import wandb


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def go(args: argparse.Namespace) -> None:
    """
    Run the basic data cleaning step:

    - Download the input artifact from W&B.
    - Filter out rows with prices outside [min_price, max_price].
    - Parse dates into datetime.
    - Save the cleaned CSV and log it back to W&B as a new artifact.
    """
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(vars(args))

    logger.info("Downloading input artifact: %s", args.input_artifact)
    artifact = run.use_artifact(args.input_artifact)
    input_path = artifact.file()

    logger.info("Reading input data from %s", input_path)
    df = pd.read_csv(input_path)

    # 1. Filter by price range
    logger.info(
        "Filtering rows with price between %s and %s",
        args.min_price,
        args.max_price,
    )
    price_filter = df["price"].between(args.min_price, args.max_price)
    df = df.loc[price_filter].copy()

    # 2. Convert last_review to datetime if present
    if "last_review" in df.columns:
        logger.info("Converting last_review to datetime")
        df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")

    # (Later in the project you’ll add geographic filtering here)

    # 3. Save cleaned data locally
    cleaned_filename = "clean_sample.csv"
    logger.info("Saving cleaned data to %s", cleaned_filename)
    df.to_csv(cleaned_filename, index=False)

    # 4. Log cleaned data as a W&B artifact
    logger.info(
        "Uploading cleaned artifact %s (type=%s) to W&B",
        args.output_artifact,
        args.output_type,
    )
    cleaned_artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    cleaned_artifact.add_file(cleaned_filename)
    run.log_artifact(cleaned_artifact)

    # Make sure upload completes before exiting
    cleaned_artifact.wait()
    logger.info("basic_cleaning step completed successfully.")


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the basic_cleaning step.
    """
    parser = argparse.ArgumentParser(
        description="Clean the raw NYC Airbnb data and log a cleaned artifact to W&B."
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        required=True,
        help="Fully qualified name of the input artifact in W&B "
             "(e.g. 'sample.csv:latest').",
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        required=True,
        help="Name for the cleaned data artifact to create in W&B "
             "(e.g. 'clean_sample.csv').",
    )

    parser.add_argument(
        "--output_type",
        type=str,
        required=True,
        help="Artifact type for the cleaned data (e.g. 'clean_sample').",
    )

    parser.add_argument(
        "--output_description",
        type=str,
        required=True,
        help="Short description of what the cleaned artifact contains.",
    )

    parser.add_argument(
        "--min_price",
        type=float,
        required=True,
        help="Minimum allowed price; rows with price lower than this are dropped.",
    )

    parser.add_argument(
        "--max_price",
        type=float,
        required=True,
        help="Maximum allowed price; rows with price higher than this are dropped.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    go(args)
