# src/fpe_encryption.py
"""
Format‑preserving encryption (FPE) helpers.Takes a DataFrame that already
contains a clean_credit_card_number column (numeric PANs as strings),
encrypts each value with the FF1 algorithm via pyffx, and returns the same
DataFrame with a new fpe_token column.
"""
import pyffx
from .logger_config import setup_logger
import pandas as pd
from typing import Union

logger = setup_logger(__name__)

# Constants
FPE_ALPHABET: str = "0123456789"  # Ensures tokens remain numeric
TOKEN_LEN: int = 20  # 16‑digit PAN → 20‑digit token for demo


def format_preserving_encryption_tokenisation(
    cc_numbers_to_tokenise: pd.DataFrame,
    fpe_key: Union[str, bytes],
) -> pd.DataFrame:
    """
    Performs format‑preserving encryption (FPE) on clean_credit_card_number.
    :param cc_numbers_to_tokenise: DataFrame that contains
    clean_credit_card_number column.
    :param fpe_key: AES‑compatible key (string or bytes) used by *pyffx*.
    :return: Original DataFrame with an extra ``fpe_token`` column.
    """

    fpe = pyffx.String(fpe_key, alphabet=FPE_ALPHABET, length=TOKEN_LEN)

    cc_numbers_to_tokenise["fpe_token"] = (
        cc_numbers_to_tokenise["clean_credit_card_number"].apply(
            lambda x: fpe.encrypt(x.zfill(TOKEN_LEN))
        )
    )

    logger.debug(
        cc_numbers_to_tokenise[[
            "credit_card_number", "clean_credit_card_number", "fpe_token"
        ]].head(10)
    )

    return cc_numbers_to_tokenise
