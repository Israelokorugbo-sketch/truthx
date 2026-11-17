import express from "express";
const app = express();
app.use(express.json());
app.get("/trade/:token", async (req,res)=>{
  const eye = await fetch("http://localhost:3001/verify/"+req.params.token).then(r=>r.json()).catch(()=>({truth_verified:true}));
  if(!eye.truth_verified) return res.json({trade:"BLOCKED", reason:"No truth = no trade"});
  res.json({ company:"SOVEREIGN HOLDINGS - SOVEREIGNX EXCHANGE", token:req.params.token, backed_by:"real_silo", treasury_fee:"goes_to_treasury", truth:eye, status:"TRADE_APPROVED" });
});
app.listen(3002, ()=>console.log("SOVEREIGNX EXCHANGE API RUNNING 3002"));