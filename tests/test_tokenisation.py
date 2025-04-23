# tests/test_tokenisation.py
"""
test tokenisation
"""
import base64
import re

import pytest

from src import aes_encryption, fpe_encryption
from src import main as main_mod
from src import simulated_data


@pytest.fixture(scope="module")
def sample_df():
    """
    Generate a tiny, deterministic dataset for repeatable tests.
    :return: DataFrame with credit card numbers
    """
    return simulated_data.create_data_to_be_tokenised(sample_size=5, seed=42)


def test_simulated_data_structure(sample_df):
    """
    The simulator should always return three well‑typed columns.
    :param sample_df: DataFrame with credit card numbers
    :return: None
    """
    assert set(sample_df.columns) == {
        "policy_id",
        "credit_card_number",
        "expiration_date",
    }
    # basic sanity checks
    assert len(sample_df) == 5
    assert sample_df["policy_id"].str.len().eq(9).all()
    assert sample_df["credit_card_number"].str.isnumeric().all()


def test_fix_cc_length_issues(sample_df):
    """
    Credit‑card numbers must be padded to 16 digits in clean column.
    :param sample_df: DataFrame with credit card numbers
    :return: None
    """
    cleaned = main_mod.fix_cc_length_issues(sample_df.copy())
    assert cleaned["clean_credit_card_number"].str.len().eq(16).all()
    # original column is untouched
    assert "clean_credit_card_number" in cleaned.columns


def test_aes_roundtrip(sample_df):
    """
    AES tokenisation should round‑trip: decrypt(encrypt(x)) == x.
    :param sample_df: DataFrame with credit card numbers
    :return: None
    """
    row = sample_df.iloc[0]
    cc = row["credit_card_number"].zfill(16)
    token_with_key = aes_encryption.encrypt_cc_number(cc)  # returns token|key
    token, b64key = token_with_key.split("|")
    key = base64.b64decode(b64key)
    plaintext = aes_encryption.decrypt_cc_number(token, key)
    assert plaintext == cc


def test_fpe_token_length(sample_df):
    """
    FPE tokens should have the length declared in fpe_encryption.TOKEN_LEN.
    :param sample_df: DataFrame with credit card numbers
    :return: None
    """
    df = main_mod.fix_cc_length_issues(sample_df.copy())
    tokenised = fpe_encryption.format_preserving_encryption_tokenisation(
        df, b"mysecretkey12345"
    )
    assert tokenised["fpe_token"].str.len().eq(fpe_encryption.TOKEN_LEN).all()
    # Ensure tokens are numeric to satisfy format‑preservation promise
    numeric_re = re.compile(r"^\d+$")
    assert tokenised["fpe_token"].apply(lambda s: bool(numeric_re.match(s))).all()
