(() => {
 const el=id=>document.getElementById(id);
 const api=el("preflight").dataset.endpoint;
 function request() {
  const target=el("target").value.trim();
  let url;try{url=new URL(target);}catch{throw Error("Enter a valid public HTTP or HTTPS MCP endpoint.");}
  if(!["https:","http:"].includes(url.protocol)||url.username||url.password)throw Error("Enter a public HTTP or HTTPS endpoint without credentials.");
  const names=[...new Set(el("tools").value.split(",").map(x=>x.trim()).filter(Boolean))];
  if(names.length>100||names.some(x=>x.length>128))throw Error("Use up to 100 tool names, each at most 128 characters.");
  const body={target_url:target,check_profile:"basic",...(names.length?{required_tools:names}:{})};
  el("request").textContent=JSON.stringify(body,null,2);return body;
 }
 const target=new URLSearchParams(location.search).get("target");
 if(target){try{const u=new URL(target);if(["https:","http:"].includes(u.protocol)&&!u.username&&!u.password)el("target").value=target;}catch{}}
 el("build").onclick=()=>{try{request();}catch(e){el("request").textContent=e.message;}};
 el("download").onclick=()=>{try{
  const body=request();const blob=new Blob([JSON.stringify(body,null,2)+"\n"],{type:"application/json"});
  const url=URL.createObjectURL(blob);const a=document.createElement("a");a.href=url;a.download="request.json";a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
 }catch(e){el("request").textContent=e.message;}};
 el("preflight").onclick=async()=>{const button=el("preflight");if(button.disabled)return;
  try{
   const body=request();button.disabled=true;el("free-result").textContent="Checking the endpoint. This is free and creates no payment.";
   const response=await fetch(api,{method:"POST",headers:{"content-type":"application/json","x-proofrail-source":"github-pages"},body:JSON.stringify({target_url:body.target_url}),signal:AbortSignal.timeout(25000)});
   const result=await response.json();
   if(!response.ok)throw Error("Free check unavailable (HTTP "+response.status+"). Retry later or use the HTTP instructions below.");
   el("free-result").textContent=JSON.stringify(result.preflight,null,2);
  }catch(e){el("free-result").textContent=e.message||"Free check failed. Try the HTTP instructions below.";}
  finally{button.disabled=false;}
 };
})();