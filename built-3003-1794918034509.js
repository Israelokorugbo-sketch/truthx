import express from "express"; import crypto from "crypto";
const chain = express();
chain.use(express.json());
const ledger=[];
chain.post("/hash", (req,res)=>{
  const hash=crypto.createHash("sha256").update(JSON.stringify(req.body)).digest("hex");
  ledger.push({hash, data:req.body, time:Date.now()});
  res.json({ company:"SOVEREIGN HOLDINGS - SOVEREIGN CHAIN L1", hash, truth_gas:true, ledger_len:ledger.length });
});
chain.listen(3003, ()=>console.log("SOVEREIGN CHAIN L1 RUNNING 3003 - TRUTH IS GAS"));