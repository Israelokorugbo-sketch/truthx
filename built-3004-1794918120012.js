import express from "express";
const coin = express();
coin.get("/", (req,res)=>res.json({ name:"TRUTH COIN", symbol:"TRUTH", isGas:true, isMoney:true, company:"SOVEREIGN HOLDINGS", treasury:true, value:"truth_is_money" }));
coin.listen(3004, ()=>console.log("TRUTH COIN RUNNING 3004"));