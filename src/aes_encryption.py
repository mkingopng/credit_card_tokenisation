# src/aes_encryption.py
"""

"""
from __future__ import annotations

import base64
import os
from typing import ByteString

import pandas as pd
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from tqdm import tqdm

from .logger_config import setup_logger

tqdm.pandas()
logger = setup_logger(__name__)

BLOCK_SIZE = 128
IV_BYTES: int = BLOCK_SIZE // 8
KEY_BYTES: int = 32


def aes_cc_tokenisation(cc_numbers_to_tokenise: pd.DataFrame) -> pd.DataFrame:
    """
    Function to tokenise credit card numbers using AES encryption.
    :param cc_numbers_to_tokenise: DataFrame containing credit card numbers to be tokenised
    :return: DataFrame with tokenised credit card numbers
    """
    logger.info("******** : AES Tokenisation : ********")
    cc_numbers_to_tokenise["aes_token"] = cc_numbers_to_tokenise[
        "clean_credit_card_number"
    ].apply(lambda x: encrypt_cc_number(x))
    logger.debug(
        cc_numbers_to_tokenise[
            ["credit_card_number", "clean_credit_card_number", "aes_token"]
        ].head(10)
    )
    return cc_numbers_to_tokenise


def encrypt_cc_number(
    cc_number: str, key: ByteString | bytes | bytearray | None = None
) -> str:
    """
    Encrypts a credit card number using AES encryption.
    :param cc_number: Credit card number to encrypt
    :param key: Key used for encryption
    :return: Encrypted credit card number as a base64 encoded string
    """
    if key is None:
        key = os.urandom(KEY_BYTES)
        return_with_key = True
    else:
        if len(key) not in {16, 24, 32, KEY_BYTES}:
            raise ValueError("Key length must be 16, 24 or 32 bytes for AES.")
        return_with_key = False

    # Pad data
    padder = padding.PKCS7(BLOCK_SIZE).padder()
    padded = padder.update(cc_number.encode()) + padder.finalize()

    # Fresh IV per encryption
    iv = os.urandom(IV_BYTES)

    # AES-CBC encrypt
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    ciphertext = cipher.encryptor().update(padded) + cipher.encryptor().finalize()

    token = base64.b64encode(iv + ciphertext).decode()
    if return_with_key:
        token += "|" + base64.b64encode(key).decode()
        logger.warning("Key returned in token – for demo use only!")

    return token


def decrypt_cc_number(token: str, key: ByteString | bytes | bytearray) -> str:
    """
    Decrypts a tokenised credit card number using AES decryption.
    :param token: Tokenised credit card number to decrypt
    :param key: Key used for decryption
    :return: Decrypted plain text credit card number
    """
    token_bytes = base64.b64decode(token)
    iv, ciphertext = token_bytes[:IV_BYTES], token_bytes[IV_BYTES:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(BLOCK_SIZE).unpadder()
    data = unpadder.update(padded) + unpadder.finalize()
    return data.decode()
