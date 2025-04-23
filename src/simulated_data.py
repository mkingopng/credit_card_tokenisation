# src/simulated_data.py
"""
Generate synthetic policy IDs, credit-card numbers, and expiry dates
for tokenisation demos or tests.
"""
from __future__ import annotations

import random
from datetime import datetime, timedelta

import pandas as pd

from src.logger_config import setup_logger

POLICY_LEN = 9
PAN_LENGTHS = (14, 15, 16)
EXPIRY_YEARS = 5

logger = setup_logger(__name__)


def create_data_to_be_tokenised(
    sample_size: int, seed: int | None = None
) -> pd.DataFrame:
    """
    Generate sample_size dummy records.
    :param sample_size: Number of rows to create
    :param seed: Optional RNG seed for reproducible tests
    :return: DataFrame with columns policy_id, credit_card_number, expiration_date
    """
    if seed is not None:
        random.seed(seed)

    records = _generate_bulk(sample_size)
    df = pd.DataFrame(records)
    logger.debug("Generated %d rows\n%s", len(df), df.head(5).to_string(index=False))
    return df


# ---------- helpers ----------


def _generate_policy_id() -> str:
    """
    Generate a random policy ID with a length of 9 digits.
    """
    return "".join(random.choices("0123456789", k=POLICY_LEN))


def _generate_credit_card_number() -> str:
    """
    Generate a random credit card number with a length of 14, 15, or 16 digits.
    :return: Credit card number as a string
    """
    return "".join(random.choices("0123456789", k=random.choice(PAN_LENGTHS)))


def _generate_expiration_date() -> str:
    """
    Generate a random expiration date in the format MM/YY.
    :return: Expiration date as a string in the format MM/YY
    """
    future = datetime.today() + timedelta(days=random.randint(365, EXPIRY_YEARS * 365))
    return future.strftime("%m/%y")


def _generate_bulk(count: int) -> list[dict[str, str]]:
    """
    Generate a list of dictionaries with dummy data.
    :param count: Number of records to generate
    :return: List of dictionaries with keys policy_id, credit_card_number, expiration_date
    """
    return [
        {
            "policy_id": _generate_policy_id(),
            "credit_card_number": _generate_credit_card_number(),
            "expiration_date": _generate_expiration_date(),
        }
        for _ in range(count)
    ]
