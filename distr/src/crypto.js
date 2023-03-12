import secp256k1 from "secp256k1";
import crypto from "crypto";

export function verifySignature(
  publicKeyHexStr,
  signatureHexDERStr,
  messageStr
) {
  if (!publicKeyHexStr.startsWith("04")) {
    publicKeyHexStr = `04${publicKeyHexStr}`;
  }
  const messageHashHexString = crypto
    .createHash("sha256")
    .update(messageStr)
    .digest()
    .toString("hex");
  const signatureUint8Array = fromHexString(signatureHexDERStr);
  const parsedSignature = secp256k1.signatureImport(signatureUint8Array);
  const normalizedSignature = secp256k1.signatureNormalize(parsedSignature);
  const publicKey = fromHexString(publicKeyHexStr);
  const messageHash = fromHexString(messageHashHexString);
  return secp256k1.ecdsaVerify(normalizedSignature, messageHash, publicKey);
}

const fromHexString = (hexString) =>
  Uint8Array.from(hexString.match(/.{1,2}/g).map((byte) => parseInt(byte, 16)));

// console.log(
//   verifySignature(
//     "01ec36537e5729e6f86a9f08cc77a6fb5a8990b327e870413b02cac8c253079fbb6dd910611fc803247587372f0a34bf871d798493efbe88f1321259686e3b1d",
//     "3045022065679d8d15a501a8787d6f3380c435e849de8c07e39f9d0efe955f50988ae3950221009593624c6eaf5cbdc10832d63c08bee3a9fce36df4d42416724cd2956feae417",
//     "caos"
//   )
// );
