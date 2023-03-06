import * as secp from "@noble/secp256k1";
import crypto from "crypto";

export async function verifySignature(publicKeyStr, signatureStr, messageStr) {
  const messageHash = await secp.utils.sha256(messageStr);
  const signature = Buffer.from(signatureStr, "hex");
  const publicKey = Buffer.from(publicKeyStr, "hex");
  return secp.verify(signature, messageHash, publicKey);
}

// NOTE: used for manual testing
async function example(name, author, version, privkey) {
  const msg = `${name}${author}${version}`;

  // // Generate a new ECDSA key pair
  const ec = crypto.createECDH("secp256k1");
  ec.generateKeys();
  const privateKey = privkey ? Buffer.from(privkey, "hex") : ec.getPrivateKey();

  const messageHash = await secp.utils.sha256(msg);

  const publicKey = secp.getPublicKey(privateKey);
  const signature = await secp.sign(messageHash, privateKey);

  console.log("Public key: ", Buffer.from(publicKey).toString("hex"));
  console.log("Private key: ", privateKey.toString("hex"));
  console.log("Signature: ", Buffer.from(signature).toString("hex"));
}

// await example("lala", "bjelicaluka", "1.0.1", "4d1305cb806a398bbc31a99989cbea0f2d0ddd82681d7ce3105f996c867e1870");
