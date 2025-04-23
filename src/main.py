# src/main.py
"""
    @Name: Credit Card Tokenisation
    @Author: Noel Singh
    @Description:
    The following application is used to tokenise credit card number using a AES Encryption method and FPE Encryption.

    AES Encryption
    AES is a symmetric-key block cipher — meaning it uses the same key for both encryption and decryption. It is widely used due to its strength and efficiency in modern cryptographic applications.
    Symmetric-key: The same key encrypts and decrypts.
    Block cipher: It encrypts data in fixed-size blocks (typically 128 bits or 16 bytes).
    Key sizes: AES supports key lengths of 128, 192, or 256 bits.

    FPE Encryption
    Format-Preserving Encryption (FPE) is a class of encryption algorithms where the ciphertext has the same format as the plaintext.
    ✅ Tokenization with reversibility
    ✅ Keeps legacy systems happy (they expect data of certain lengths/formats)
    ✅ No schema changes needed in databases (because formats don’t change)
    ✅ PCI compliance friendliness (often used in credit card/token vaults)

    FPE encrypts data while respecting a specific format using standard block ciphers like AES under the hood — it wraps these in special constructions like:
    FF1 / FF3: NIST-approved algorithms for FPE over strings/numbers
    Feistel networks: for splitting and recombining data in predictable formats
"""
import warnings

import pandas as pd
from tqdm import tqdm

from src import aes_encryption, fpe_encryption, simulated_data
from src.logger_config import setup_logger

tqdm.pandas()
warnings.filterwarnings("ignore")
logger = setup_logger(__name__)
FPE_KEY = b"mysecretkey12345"  # FPE Encryption Key


def data_exploration(cc_numbers_to_tokenise: pd.DataFrame) -> str:
    """
    Validate policy IDs & credit‑card numbers and report a status string.
    :param cc_numbers_to_tokenise: DataFrame containing raw inputs
    :return: ``"Errors"`` if any issues detected, otherwise ``"No_Errors"``
    """
    logger.info("******** : Checking Data to Tokenise : ********")
    invalid_pol = policy_id_checks(cc_numbers_to_tokenise)
    invalid_cc = cc_number_checks(cc_numbers_to_tokenise)
    total_rows_with_special = check_special_characters(cc_numbers_to_tokenise)

    if len(invalid_pol) != 0 or len(invalid_cc) != 0 or total_rows_with_special != 0:
        status = "Errors"
    else:
        status = "No_Errors"
    return status


def policy_id_checks(data: pd.DataFrame) -> list:
    """
    Check the character length of each field in all records.
    :param data: DataFrame containing the data to be checked
    :return: List of indices of records with invalid policy IDs
    """
    logger.info("----- : Policy ID Checks : -----")
    invalid_pol = []
    for index, row in data.iterrows():
        pol_len = len(row["policy_id"])
        if pol_len != 9:
            invalid_pol.append(index)

    if len(invalid_pol) > 0:
        logger.warning(invalid_pol)
    else:
        logger.debug("No data length issues found")
    return invalid_pol


def cc_number_checks(data: pd.DataFrame) -> list:
    """
    Check the character length of each field in all records.
    :param data: DataFrame containing the data to be checked
    :return: List of indices of records with invalid credit card numbers
    """
    logger.info("----- : Credit Card Checks : -----")
    invalid_cc = []
    for index, row in data.iterrows():
        cc_len = len(row["credit_card_number"])
        if cc_len < 16:
            invalid_cc.append(index)

    # If Errors Found Report
    if len(invalid_cc) > 0:
        # logger.warning(invalid_cc)
        logger.debug(f"Total CC Length Errors: {len(invalid_cc)}")
    else:
        logger.debug("No data length issues found")
    return invalid_cc


def check_special_characters(data: pd.DataFrame) -> list:
    """
    Check for special characters in 'policy_id' and 'credit_card_number' fields.
    :param data: DataFrame containing the data to be checked
    :return: List of indices of records with special characters
    """
    logger.info("----- : Checking for Special Characters : -----")
    special_char_pattern = r"[^A-Za-z0-9]"
    # Check for special characters in 'policy_id' and 'credit_card_number'
    data["policy_id_has_special"] = data["policy_id"].str.contains(special_char_pattern)
    data["card_has_special"] = data["credit_card_number"].str.contains(
        special_char_pattern
    )

    # Count of rows with special characters in each column
    policy_id_special_count = data["policy_id_has_special"].sum()
    card_special_count = data["card_has_special"].sum()

    # Total rows with special characters in either field
    total_rows_with_special = (
        data["policy_id_has_special"] | data["card_has_special"]
    ).sum()

    logger.debug(
        f"Total Errors: {total_rows_with_special} \n"
        f"Total Policy Number: {policy_id_special_count} \n"
        f"Total CC Number: {card_special_count}"
    )
    return total_rows_with_special


def clean_data_before_tokenisation(
    cc_numbers_to_tokenise: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean the data before tokenisation.
    :param cc_numbers_to_tokenise: DataFrame containing the data to be cleaned
    :return: Cleaned DataFrame
    """
    logger.info("******** : Checking Data to Tokenise : ********")
    # cc_numbers_to_tokenise = remove_white_spaces(cc_numbers_to_tokenise)
    cc_numbers_to_tokenise = fix_cc_length_issues(cc_numbers_to_tokenise)

    return cc_numbers_to_tokenise


def remove_white_spaces(cc_numbers_to_tokenise):
    """
    Remove white spaces from credit card numbers.
    :param cc_numbers_to_tokenise: DataFrame containing the data to be cleaned
    :return: Cleaned DataFrame
    """
    logger.debug("Removing White spaces from credit card numbers")
    # TODO: Complete functionality


def fix_cc_length_issues(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pad all credit-card numbers to 16 digits in a new
    `clean_credit_card_number` column (leaves originals untouched).
    """
    df["clean_credit_card_number"] = df["credit_card_number"].astype(str).str.zfill(16)
    return df


def main(
    run_type: str = "SIM", encryption_method: str = "FPE", sample_size: int = 18_000
) -> None:
    """
    Driver function; supports SIMulated data only for now.
    :param run_type: Type of run (e.g., "SIM" for simulated data)
    :param encryption_method: Encryption method to use (e.g., "FPE" or "AES")
    :param sample_size: Number of records to simulate
    :return: None
    """
    if run_type != "SIM":
        logger.error("Only SIM run_type is supported in this demo.")
        return

    # --- generate synthetic data ---
    cc_numbers_to_tokenise = simulated_data.create_data_to_be_tokenised(
        sample_size=sample_size
    )
    cc_numbers_to_tokenise = clean_data_before_tokenisation(cc_numbers_to_tokenise)

    if encryption_method.upper() == "FPE":
        _ = fpe_encryption.format_preserving_encryption_tokenisation(
            cc_numbers_to_tokenise, FPE_KEY
        )
    elif encryption_method.upper() == "AES":
        # NOTE: aes_cc_tokenisation processes the DataFrame row‑wise
        _ = aes_encryption.aes_cc_tokenisation(cc_numbers_to_tokenise)
    else:
        logger.error("Invalid encryption_method; choose FPE or AES.")


if __name__ == "__main__":
    main()
