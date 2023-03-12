from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey


def generate_keys():
  private_key = PrivateKey()
  return private_key.toString(), private_key.publicKey().toString()


def sign_message(private_key_hex_string: str, message: str):
  privateKey = PrivateKey.fromString(private_key_hex_string)
  return Ecdsa.sign(message, privateKey).toDer().hex()

