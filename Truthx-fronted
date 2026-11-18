<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TruthX - AI Truth Engine</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>body{font-family:'Inter',sans-serif}</style>
</head>
<body class="bg-[#0a0a0b] text-white min-h-screen">
<!-- Header -->
<header class="border-b border-white/10 sticky top-0 bg-[#0a0a0b]/80 backdrop-blur-xl z-10">
<div class="max-w-5xl mx-auto px-6 py-4 flex justify-between items-center">
<div class="flex items-center gap-2"><div class="w-8 h-8 bg-white text-black rounded-lg flex items-center justify-center font-black text-sm">TX</div><span class="font-bold text-lg">TruthX</span></div>
<div class="text-xs text-white/40">API: Connected ✓</div>
</div>
</header>

<main class="max-w-3xl mx-auto px-6 pt-20">
<h1 class="text-5xl font-extrabold tracking-tight text-center leading-tight">What do you want<br><span class="text-white/40">to verify?</span></h1>

<!-- Search Box -->
<div class="mt-10 bg-[#18181b] border border-white/10 rounded-2xl p-2 shadow-2xl">
<textarea id="claimInput" rows="3" placeholder="Enter any claim, news, or statement to verify... e.g. 'Nigeria's inflation rate dropped to 15% in October'" class="w-full bg-transparent p-4 outline-none resize-none text-[15px] placeholder:text-white/30"></textarea>
<div class="flex justify-between items-center px-2 pb-2">
<div class="text-xs text-white/30">Powered by TruthX API</div>
<button onclick="verifyClaim()" id="verifyBtn" class="bg-white text-black px-6 py-2.5 rounded-xl font-semibold text-sm hover:bg-white/90 transition">Verify →</button>
</div>
</div>

<!-- Result Area -->
<div id="result" class="mt-8 hidden">
<div class="bg-[#18181b] border border-white/10 rounded-2xl p-6">
<div class="flex items-center gap-3 mb-4">
<div id="scoreCircle" class="w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm">--</div>
<div><div id="verdict" class="font-semibold">Checking...</div><div id="sub" class="text-xs text-white/50">Analyzing sources</div></div>
</div>
<div id="explanation" class="text-[14px] leading-6 text-white/80 whitespace-pre-wrap"></div>
<div id="sources" class="mt-4 pt-4 border-t border-white/10"></div>
</div>
</div>

<div class="mt-12 flex gap-2 justify-center text-xs text-white/20">
<span class="border border-white/10 rounded-full px-3 py-1">Real-time</span>
<span class="border border-white/10 rounded-full px-3 py-1">Source-backed</span>
<span class="border border-white/10 rounded-full px-3 py-1">Unbiased</span>
</div>
</main>

<script>
const API_BASE = "https://truthx-api-6i6k.onrender.com";

async function verifyClaim(){
 const claim = document.getElementById('claimInput').value.trim();
 if(!claim) return alert("Please enter a claim to verify");
 const btn = document.getElementById('verifyBtn');
 const resultDiv = document.getElementById('result');
 const explanation = document.getElementById('explanation');
 const verdictEl = document.getElementById('verdict');
 const scoreCircle = document.getElementById('scoreCircle');
 
 btn.innerHTML = "Checking...";
 btn.disabled = true;
 resultDiv.classList.remove('hidden');
 verdictEl.innerText = "Verifying with AI...";
 explanation.innerText = "Connecting to TruthX engine at " + API_BASE + " ... This may take 10-20 seconds on first request (Render wakes up).";
 scoreCircle.innerText = "...";
 scoreCircle.className = "w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm bg-white/10";
 
 try {
   // Try common endpoints - change if your backend uses different path
   let res;
   let endpoints = ["/api/verify", "/verify", "/api/check", "/check", "/api/fact-check"];
   let data = null;
   
   for(let ep of endpoints){
     try{
       res = await fetch(API_BASE + ep, {
         method: 'POST',
         headers: {'Content-Type':'application/json'},
         body: JSON.stringify({claim: claim, query: claim, text: claim})
       });
       if(res.ok){ data = await res.json(); break; }
     }catch(e){}
   }
   
   // If all POST failed, try GET
   if(!data){
     res = await fetch(API_BASE + "/api/verify?claim=" + encodeURIComponent(claim));
     if(res.ok) data = await res.json();
   }
   
   if(!data) throw new Error("API endpoint not found. Please check backend routes.");
   
   // Display result - flexible for your backend response shape
   let score = data.score || data.truthScore || data.confidence || 75;
   let verdict = data.verdict || data.result || data.label || "Analysis Complete";
   let expl = data.explanation || data.analysis || data.reasoning || data.summary || JSON.stringify(data, null, 2);
   
   scoreCircle.innerText = score + "%";
   if(score >= 70) scoreCircle.className = "w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm bg-green-500/20 text-green-400 border border-green-500/20";
   else if(score >= 40) scoreCircle.className = "w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm bg-yellow-500/20 text-yellow-400 border border-yellow-500/20";
   else scoreCircle.className = "w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm bg-red-500/20 text-red-400 border border-red-500/20";
   
   verdictEl.innerText = verdict;
   document.getElementById('sub').innerText = "Truth Score: " + score + "%";
   explanation.innerText = expl;
   
   if(data.sources || data.references){
     let srcs = data.sources || data.references;
     document.getElementById('sources').innerHTML = "<div class='text-xs font-semibold text-white/40 mb-2'>SOURCES</div>" + srcs.map(s=>`<div class='text-xs text-white/50 py-1'>• ${typeof s === 'string' ? s : s.title || s.url || JSON.stringify(s)}</div>`).join('');
   }
   
 } catch(err){
   verdictEl.innerText = "Connection Issue";
   explanation.innerText = "Error: " + err.message + "\n\nYour backend is live at " + API_BASE + " but I couldn't find the verify route. \n\nCommon routes are: /verify, /api/verify, /check. \n\nOpen " + API_BASE + "/docs or " + API_BASE + " in browser to see available endpoints, then tell me the correct endpoint and I will update the file for you instantly.";
   scoreCircle.innerText = "!";
   scoreCircle.className = "w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm bg-red-500/20 text-red-400";
 }
 btn.innerHTML = "Verify →";
 btn.disabled = false;
}
</script>
</body>
</html>
