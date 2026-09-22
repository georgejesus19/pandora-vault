import secrets
import src.crypto.kfd as kfd
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NONCE_LENGTH = 12
AUTH_TAG_LENGTH = 16

DEFAULT_MEMORY_COST = kfd.DEFAULT_MEMORY_COST
DEFAULT_TIME_COST = kfd.DEFAULT_TIME_COST
DEFAULT_PARALLELISM = kfd.DEFAULT_PARALLELISM
SALT_LENGTH = kfd.SALT_LENGTH


def encrypt(key, plaintext):
    """
    :param key: derived key generate with kfd
    :param plaintext: data to encrypt
    :return: dictionary with ciphertext, nonce and authentication tag
    """
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(NONCE_LENGTH)
    encrypted_data = aesgcm.encrypt(nonce, plaintext, None)
    ciphertext = encrypted_data[:-AUTH_TAG_LENGTH]
    authentication_tag = encrypted_data[-AUTH_TAG_LENGTH:]

    return {"ciphertext": ciphertext,
            "nonce": nonce,
            "authentication_tag": authentication_tag}

def decrypt(key, nonce, ciphertext, authentication_tag):
    """
    :param key: Derived key generate with kfd
    :param nonce: unique value generated during encryption
    :param ciphertext: ciphertext generated during encryption
    :param authentication_tag: authentication tag generated during encryption
    :return: The decrypted plaintext
    """
    aesgcm = AESGCM(key)
    encrypted_data = ciphertext + authentication_tag
    desencrypted_data = aesgcm.decrypt(nonce, encrypted_data,None)
    return desencrypted_data