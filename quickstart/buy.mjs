// One purchase only. Default is a quote; --pay explicitly authorizes 0.10 USDC.
import {readFile, writeFile, access} from "node:fs/promises";
import {x402Client} from "@x402/core/client";
import {decodePaymentRequiredHeader, encodePaymentSignatureHeader, decodePaymentResponseHeader} from "@x402/core/http";
import {ExactEvmScheme} from "@x402/evm/exact/client";
import {privateKeyToAccount} from "viem/accounts";
const endpoint = "https://drkdm4jd-8767.uks1.devtunnels.ms/api/certify";
const filename = process.argv[2];
if (!filename || filename.startsWith("--")) throw Error("Usage: node buy.mjs request.json [--pay]");
const body = JSON.stringify(JSON.parse(await readFile(filename, "utf8")));
const headers = {"content-type":"application/json","user-agent":"proofrail-buyer-example/0.4.0","x-proofrail-source":"direct"};
const quote = await fetch(endpoint, {method:"POST",headers,body,redirect:"error",signal:AbortSignal.timeout(30000)});
if (quote.status !== 402 || !quote.headers.has("payment-required")) throw Error("Quote failed: HTTP "+quote.status+" "+await quote.text());
const required = decodePaymentRequiredHeader(quote.headers.get("payment-required"));
const allowed = required.accepts.filter(a => a.scheme === "exact" && a.network === "eip155:8453" && a.amount === "100000" && a.asset.toLowerCase() === "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913" && a.payTo.toLowerCase() === "0x865fc95cb5b9767dafe07acb0e0593fb40bcc28c");
if (required.x402Version !== 2 || required.resource?.url !== endpoint || allowed.length !== 1) throw Error("Unexpected payment terms; no authorization created.");
console.log(JSON.stringify({price:"0.10 USDC",network:allowed[0].network,payTo:allowed[0].payTo,willPay:process.argv.includes("--pay")},null,2));
if (process.argv.includes("--pay")) {
  try { await access("proofrail-result.json"); throw Error("Move existing proofrail-result.json before authorizing another purchase."); } catch (e) { if (e.code !== "ENOENT") throw e; }
  const key = process.env.PROOFRAIL_BUYER_KEY;
  if (!key || !/^0x[0-9a-fA-F]{64}$/.test(key)) throw Error("Set PROOFRAIL_BUYER_KEY locally to your buyer wallet private key.");
  const client = new x402Client().register("eip155:8453",new ExactEvmScheme(privateKeyToAccount(key)));
  const payload = await client.createPaymentPayload({...required,accepts:allowed});
  const response = await fetch(endpoint,{method:"POST",headers:{...headers,"PAYMENT-SIGNATURE":encodePaymentSignatureHeader(payload)},body,redirect:"error",signal:AbortSignal.timeout(60000)});
  const result = await response.text();
  await writeFile("proofrail-result.json",result,{flag:"wx"});
  const settlementHeader = response.headers.get("payment-response");
  const settled = settlementHeader ? decodePaymentResponseHeader(settlementHeader) : null;
  if (!response.ok || !settled?.success) throw Error("Check proofrail-result.json and your wallet before any retry; settlement is not confirmed. HTTP "+response.status);
  console.log("Result saved in proofrail-result.json. Transaction: "+settled.transaction);
}
