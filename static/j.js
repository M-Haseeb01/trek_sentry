/* Load values */

const countrySelect = document.getElementById("country");
const cityInput = document.getElementById("city");
const suggestions = document.getElementById("suggestions");
const output = document.getElementById("output");
const translated = document.getElementById("translated");
const audio = document.getElementById("audio");
const btn = document.getElementById("analyzeBtn");
const btnText = document.getElementById("btnText");
const spinner = document.getElementById("spinner");
const langSelect = document.getElementById("lang");
const translateBox = document.getElementById("translateBox");
const translateBtn = document.getElementById("translateBtn");
const audioBtn = document.getElementById("audioBtn");

/* Load countries */

fetch("/api/countries").then(r=>r.json()).then(data=>{
  data.forEach(c=>{
    const opt=document.createElement("option");
    opt.value=c.name;
    opt.textContent=c.name;
    countrySelect.appendChild(opt);
  });
});

/* Load languages */

fetch("/api/languages").then(r=>r.json()).then(data=>{
  data.forEach(l=>{
    const opt=document.createElement("option");
    opt.value=l.code;
    opt.textContent=l.name;
    langSelect.appendChild(opt);
  });
});

/* City autocomplete */

cityInput.addEventListener("input", async ()=>{
  const q=cityInput.value;
  const country=countrySelect.value;
  if(q.length<2){ suggestions.innerHTML=""; suggestions.style.display="none"; return; }

  const res = await fetch(`/api/search-city?q=${q}&country=${country}`);
  const cities = await res.json();

  suggestions.innerHTML="";
  if(cities.length) suggestions.style.display="block"; else suggestions.style.display="none";
  cities.forEach(city=>{
    const li=document.createElement("li");
    li.textContent=city;
    li.onclick=()=>{ cityInput.value=city; suggestions.innerHTML=""; suggestions.style.display="none"; };
    suggestions.appendChild(li);
  });
});

/* Analyze */

btn.addEventListener("click", async ()=>{
  btn.classList.add("loading");       
  btn.style.width = "46px";          
  btn.style.padding = "0";           
  const city=cityInput.value, country=countrySelect.value;
  try{
    const res = await fetch("/api/analyze",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({city,country})
    });
    const data = await res.json();

    output.innerHTML="";
    if(data.summary){
      const parts = data.summary.split("@");
      const headings=[" ","Situation:","Preparation:","Recommendation:"];
      parts.forEach((part,i)=>{
        const trimmed = part.trim(); if(!trimmed) return;
        const h=document.createElement("h3"); h.textContent=headings[i]||`Heading ${i+1}`;
        const p=document.createElement("p"); p.textContent=trimmed;
        output.appendChild(h); output.appendChild(p);
      });

      translateBox.style.display="flex";
      audioBtn.style.display="inline-block";
      translated.style.display="none";
      audio.src=`/api/audio?city=${encodeURIComponent(city)}&country=${encodeURIComponent(country)}`;
    } else {
      output.innerText=data.error||"No summary available";
      translateBox.style.display="none";
      translated.style.display="none";
    }
  } catch(err){
    output.innerText="Error fetching data!";
    translateBox.style.display="none";
    translated.style.display="none";
  } finally {
    btn.classList.remove("loading");    
    btn.style.width = "";               
    btn.style.padding = "";             
  }
});


/* Translate */

translateBtn.addEventListener("click", async ()=>{
  const lang = langSelect.value;
  if(!lang) return alert("Select language");

  const res = await fetch("/api/translate",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({text: output.innerText, language: lang})
  });
  const data = await res.json();
  translated.innerText = data.translated;
  translated.style.display="block";
});

/* Audio play */

audioBtn.addEventListener("click", ()=>{
  if(audio.src) audio.play();
});
