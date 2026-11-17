import express from "express";
const holdings = express();
holdings.get("/", async (req,res)=>{
  const eye = await fetch("http://localhost:3001/verify/RICE-5000KG").then(r=>r.json()).catch(()=>({error:"eye down"}));
  const trade = await fetch("http://localhost:3002/trade/RICE-5000KG").then(r=>r.json()).catch(()=>({error:"exchange down"}));
  const coin = await fetch("http://localhost:3004/").then(r=>r.json()).catch(()=>({error:"coin down"}));
  const treasury = await fetch("http://localhost:3005/").then(r=>r.json()).catch(()=>({error:"treasury down"}));
  const chain = await fetch("http://localhost:3003/ledger").then(r=>r.json()).catch(()=>({error:"chain down"}));
  res.json({
    SOVEREIGN_HOLDINGS_EMPIRE: "ALL 5 COMPANIES LIVE",
    companies: {
      "1_EARTHS_EYE_3001": eye,
      "2_SOVEREIGNX_EXCHANGE_3002": trade,
      "3_SOVEREIGN_CHAIN_L1_3003": chain,
      "4_TRUTH_COIN_3004": coin,
      "5_TREASURY_VAULT_3005": treasury
    },
    thesis: "No truth = No trade | Truth is gas | Truth is money",
    built_from: "Termux in Enugu"
  });
});
holdings.listen(5000, ()=>console.log("SOVEREIGN HOLDINGS MASTER RUNNING ON 5000 - http://localhost:5000/"));
