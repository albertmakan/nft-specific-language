import ecdsa
from hashlib import sha256

# SECP256k1 is the Bitcoin elliptic curve


def generate_key_pair():
    priv_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    pub_key = priv_key.get_verifying_key()
    return (priv_key.to_string().hex(), pub_key.to_string().hex())


def create_signature(priv_key_string, text):
    priv_key = ecdsa.SigningKey.from_string(bytes.fromhex(
        priv_key_string), curve=ecdsa.SECP256k1, hashfunc=sha256)
    return priv_key.sign(str.encode(text)).hex()


def verify_signature(pub_key_string, signature, text):
    pub_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(
        pub_key_string), curve=ecdsa.SECP256k1, hashfunc=sha256)
    return pub_key.verify(bytes.fromhex(signature), str.encode(text))


if __name__ == "__main__":
    priv, pub = generate_key_pair()
    print(priv, pub)
    signature = create_signature(priv, "panic je malo jaje")
    print(signature)
    print(verify_signature(pub, signature, "panic je malo jaje"))
    print(verify_signature(pub, signature, "panic je malo jaje INVALID"))
