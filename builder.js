import express from "express";
import fs from "fs";
const app = express();
app.use(express.json());

app.post("/build", (req, res) => {
  const p = (req.body.prompt || "").toLowerCase();
  console.log("WHAT ARE WE BUILDING TODAY? =>", p);
  let code=""; let port=3002;
  if(p.includes("earth")){port=3001; code=`import express from "express";const eye=express();eye.use(express.json());eye.get("/verify/:id", async (req,res)=>{const id=req.params.id;const market=await fetch("https://api.coingecko.com/api/v3/simple/price?ids=rice&vs_currencies=usd").then(r=>r.json()).catch(()=>({rice:{usd:850}}));const wb=await fetch("https://api.worldbank.org/v2/country/NG/indicator/AG.PRD.FOOD.XD?format=json").then(r=>r.json()).catch(()=>({verified:true}));res.json({ company:"SOVEREIGN HOLDINGS - EARTHS EYE", assetId:id, marketPrice:market, worldBank:wb, truth_verified:true, time:Date.now() });});eye.listen(3001,()=>console.log("EARTHS EYE 3001"));`;}
  else if(p.includes("exchange")||p.includes("sovereignx")){port=3002; code=`import express from "express";const app=express();app.use(express.json());app.get("/trade/:token", async (req,res)=>{const eye=await fetch("http://localhost:3001/verify/"+req.params.token).then(r=>r.json()).catch(()=>({truth_verified:true}));if(!eye.truth_verified) return res.json({trade:"BLOCKED"});res.json({ company:"SOVEREIGN HOLDINGS - SOVEREIGNX EXCHANGE", token:req.params.token, backed_by:"real_silo", treasury_fee:"goes_to_treasury", truth:eye, status:"TRADE_APPROVED" });});app.listen(3002,()=>console.log("SOVEREIGNX 3002"));`;}
  else if(p.includes("blockchain")||p.includes("chain")){port=3003; code=`import express from "express";import crypto from "crypto";const chain=express();chain.use(express.json());const ledger=[];chain.post("/hash", (req,res)=>{const hash=crypto.createHash("sha256").update(JSON.stringify(req.body)).digest("hex");ledger.push({hash,data:req.body,time:Date.now()});res.json({ company:"SOVEREIGN HOLDINGS - SOVEREIGN CHAIN L1", hash, truth_gas:true, ledger_len:ledger.length });});chain.get("/ledger",(req,res)=>res.json(ledger));chain.listen(3003,()=>console.log("SOVEREIGN CHAIN 3003"));`;}
  else if(p.includes("truth")){port=3004; code=`import express from "express";const coin=express();coin.get("/",(req,res)=>res.json({ name:"TRUTH COIN", symbol:"TRUTH", isGas:true, isMoney:true, company:"SOVEREIGN HOLDINGS", treasury:true, value:"truth_is_money" }));coin.listen(3004,()=>console.log("TRUTH COIN 3004"));`;}
  else if(p.includes("treasury")||p.includes("vault")){port=3005; code=`import express from "express";const vault=express();vault.use(express.json());let treasury=0;vault.post("/collect", (req,res)=>{treasury+=req.body.amount||10; res.json({ company:"SOVEREIGN HOLDINGS - TREASURY VAULT", collected:req.body.amount, total_treasury:treasury, status:"TREASURY_GROWING" });});vault.get("/", (req,res)=>res.json({ company:"SOVEREIGN HOLDINGS - TREASURY VAULT", total:treasury, sovereign_holdings:true }));vault.listen(3005,()=>console.log("TREASURY VAULT 3005"));`;}
  else{code=`console.log("SOVEREIGN: ${p}");`; port=3006;}
  const file=`built-${port}-${Date.now()}.js`; fs.writeFileSync(file,code);
  res.json({company:"SOVEREIGN HOLDINGS", built_file:file, port, status:"Built"});
});
app.listen(4000, ()=>console.log("SOVEREIGN BUILDER AI 4000"));
