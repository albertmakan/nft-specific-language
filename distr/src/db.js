import * as IPFS from "ipfs";
import { HttpGateway } from "ipfs-http-gateway";
import OrbitDB from "orbit-db";
import express from "express";
import z from "zod";
import { addMonths } from "date-fns";
import { testVersion, compareVersions } from "./utils.js";
import { verifySignature } from "./crypto.js";
import cors from "cors";

// TODO: implement clustering logic
// import * as PeerId from "@libp2p/peer-id";
// peers need to be connected in order to keep a constant sync
// await ipfs.swarm.connect(
//   PeerId.peerIdFromString(
//     "12D3KooWHbeEMf8iymRxkWmbV7MKYsmvqcjdnfaKH99BW9NjcqWT"
//   )
// );

const app = express();
const port = 3000;

app.use(cors());

app.use(express.static('spm-docs/build'))

app.use(express.json());

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});

const ipfs = await IPFS.create({
  repo: "./spm_db/ipfs",
  start: true,
  EXPERIMENTAL: {
    pubsub: true,
  },
  relay: {
    enabled: true, // enable circuit relay dialer and listener
    hop: {
      enabled: true, // enable circuit relay HOP (make this node a relay)
    },
  },
  config: {
    Addresses: {
      Gateway: "/ip4/0.0.0.0/tcp/9090",
    },
  },
  pubsub: true,
});

const ipfsGateway = new HttpGateway(ipfs);
await ipfsGateway.start();

const orbitdb = await OrbitDB.createInstance(ipfs, {
  directory: "./spm_db/docstore",
});

// Create / Open a database
const latestVersionsDb = await orbitdb.docs("spm:packages", {
  indexBy: "name",
  accessController: {
    write: [
      // Give access to ourselves
      orbitdb.identity.id,
    ],
  },
  overwrite: true,
  replicate: true,
});
await latestVersionsDb.load();

const allVersionsDb = await orbitdb.docs("spm:packages-all", {
  indexBy: "tag",
  accessController: {
    write: [
      // Give access to ourselves
      orbitdb.identity.id,
    ],
  },
  overwrite: true,
  replicate: true,
});
await allVersionsDb.load();

// Listen for updates from peers
latestVersionsDb.events.on("replicated", async (address) => {
  console.log("REPL_DONE: ", address);
});
allVersionsDb.events.on("replicated", async (address) => {
  console.log("REPL_DONE: ", address);
});

// API

app.get("/api/db", async (req, res) => {
  res.send({
    name: latestVersionsDb.dbname,
    address: latestVersionsDb.address.toString(),
  });
});

app.get("/api/peer", async (req, res) => {
  res.send({
    peer: await ipfs.id(),
    swarmAddrs: await ipfs.swarm.addrs(),
  });
});

app.get("/api/spm/search/:term", async (req, res) => {
  const result = await latestVersionsDb.get(req.params.term);

  res.send(result);
});

app.get("/api/spm/search", async (req, res) => {
  const result = await latestVersionsDb.get("");

  res.send(result);
});

app.get("/api/spm/package/:name", async (req, res) => {
  const result = await allVersionsDb.get(`${req.params.name}:`);

  res.send(result);
});

const createPackageSchema = z.object({
  name: z
    .string("Name is required")
    .min(3, "Name must be at least 3 characters long."),
  version: z
    .string("Version is required.")
    .min(5, "Version must be at least 5 characters long.")
    .refine((version) => {
      return testVersion(version);
    }),
  author: z
    .string("Author is required.")
    .min(4, "Author must be at least 4 characters long."),
  pubkey: z
    .string("Public key is required.")
    .min(8, "Public Key must be at least 8 characters long."),
  signature: z
    .string()
    .min(8, "Signature must be at least 8 characters long.")
    .optional(),
  content: z
    .string("Package content is required.")
    .min(10, "Package content is mandatory."),
  // meta info about the functionalities provided by the package
  meta: z.object().optional(),
  readme: z.string().optional(),
});

app.post("/api/spm/packages", async (req, res) => {
  try {
    const threeMonthsLater = addMonths(new Date(), 3);

    const parsedPackage = createPackageSchema.parse(req.body);
    const existingPackages = await latestVersionsDb.get(parsedPackage.name);
    const allExistingVersions = await allVersionsDb.get(
      parsedPackage.name + ":"
    );
    const sameVersionExists = allExistingVersions.find(
      (x) =>
        x.name === parsedPackage.name && x.version === parsedPackage.version
    );
    if (!!sameVersionExists) {
      res.status(400).send({ message: "Package version already exists" });
      return;
    }

    const existingPackage = existingPackages.find(
      (x) => x.name === parsedPackage.name
    );

    if (!parsedPackage.pubkey) {
      res
        .status(400)
        .send({ message: "Public key must be provided when publishing." });
      return;
    }
    if (
      !!existingPackage &&
      parsedPackage.pubkey !== existingPackage.pubkey &&
      new Date(existingPackage.expirationDate).getTime() >
        threeMonthsLater.getTime()
    ) {
      res.status(400).send({ message: "Package is reserved for 3 months." });
      return;
    } else if (
      !!existingPackage &&
      parsedPackage.pubkey !== existingPackage.pubkey
    ) {
      res
        .status(400)
        .send({ message: "Public key must match the previous one." });
      return;
    }

    if (!parsedPackage.signature) {
      res.status(400).send({
        message:
          "Signature must be provided when publishing a new version of the package. Signature: privkey(name + author + version).",
      });
      return;
    }
    const message = `${parsedPackage.name}${parsedPackage.author}${parsedPackage.version}`;
    const signatureValid = await verifySignature(
      parsedPackage.pubkey,
      parsedPackage.signature,
      message
    );
    if (!signatureValid) {
      res.status(400).send({
        message:
          "Invalid signature for the provided package info. Signature: privkey(name + author + version).",
      });
      return;
    }
    if (!!existingPackage) {
      if (compareVersions(existingPackage.version, parsedPackage.version)) {
        res.status(400).send({
          message:
            "Package version must be greater than the latest existing one.",
        });
        return;
      }
    }

    const result = await ipfs.add(parsedPackage.content);

    const packageToStore = {
      ...parsedPackage,
      cid: result.cid.toString(),
      expirationDate: threeMonthsLater.toISOString(),
    };
    delete packageToStore.content;

    await latestVersionsDb.put(packageToStore);
    await allVersionsDb.put({
      ...packageToStore,
      tag: `${parsedPackage.name}:${parsedPackage.version}`,
    });

    res.status(200).send(parsedPackage);
  } catch (error) {
    console.log(error);
    res.status(400).send({ message: error.message });
  }
});

process.on("SIGTERM", async (error) => {
  try {
    await ipfsGateway.stop();
    await latestVersionsDb.close();
    await orbitdb.stop();
    await ipfs.stop();
  } catch (error) {
    console.error(error);
    process.kill(9);
  }
});

process.on("SIGINT", async (error) => {
  try {
    await ipfsGateway.stop();
    await latestVersionsDb.close();
    await orbitdb.stop();
    await ipfs.stop();
  } catch (error) {
    console.error(error);
    process.kill(9);
  }
});
