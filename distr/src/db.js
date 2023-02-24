import * as IPFS from "ipfs";
import { HttpGateway } from "ipfs-http-gateway";
import OrbitDB from "orbit-db";
// import * as PeerId from "@libp2p/peer-id";
import express from "express";

const app = express();
const port = 3000;

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
  pubsub: true,
});

const ipfsGateway = new HttpGateway(ipfs);
await ipfsGateway.start();

const orbitdb = await OrbitDB.createInstance(ipfs, {
  directory: "./spm_db/docstore",
});

// TODO: implement clustering logic
// peers need to be connected in order to keep a constant sync
// await ipfs.swarm.connect(
//   PeerId.peerIdFromString(
//     "12D3KooWHbeEMf8iymRxkWmbV7MKYsmvqcjdnfaKH99BW9NjcqWT"
//   )
// );

// Create / Open a database
const db = await orbitdb.docs("spm:packages", {
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
await db.load();

// Listen for updates from peers
db.events.on("replicated", async (address) => {
  console.log("REPL_DONE: ", address);
});

// API

app.get("/api/db", async (req, res) => {
  res.send({
    name: db.dbname,
    address: db.address.toString(),
  });
});

app.get("/api/peer", async (req, res) => {
  res.send({
    peer: await ipfs.id(),
    swarmAddrs: await ipfs.swarm.addrs(),
  });
});

app.get("/api/spm/search/:term", async (req, res) => {
  const result = await db.get(req.params.term);

  res.send(result);
});

app.post("/api/spm/packages", async (req, res) => {
  // TODO: implement validation
  // TODO: check signatures if package already exists (if last renewed < 3 months)
  await db.put(req.body);
  res.sendStatus(200);
});

app.post("/api/spm/packages/:name/renew", async (req, res) => {
  // TODO: implement validation
  // TODO: check signatures
  // TODO: package can be renewed by the same signature after 2 months, and taken over by others after 3 months
  // Note: renewing means keeping the same signature for additional 3 months
  // Note: taking over means placing a new signature for that package name - IT DOES NOT mean replacing the package
  // Note: packages can't be deleted!
  await db.put(req.body);
  res.sendStatus(200);
});

process.on("SIGTERM", async (error) => {
  try {
    await ipfsGateway.stop();
    await db.close();
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
    await db.close();
    await orbitdb.stop();
    await ipfs.stop();
  } catch (error) {
    console.error(error);
    process.kill(9);
  }
});
