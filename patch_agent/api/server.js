import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';

const app = express();
app.use(express.json());
const CORS_ORIGIN = process.env.CORS_ORIGIN || 'http://localhost:5173';
app.use(cors({ origin: CORS_ORIGIN }));

const PORT = Number(process.env.API_PORT || 4000);
const BASE_PRICE = Number(process.env.BASE_PRICE || 100);
const COUPON_CODE = process.env.COUPON_CODE || 'FIXME50';
const DISCOUNT_PCT = Number(process.env.DISCOUNT_PCT || 0.5);
const BUG_MODE = String(process.env.BUG_MODE || 'true') === 'true';
const GATEWAY_URL = process.env.GATEWAY_URL || 'http://gateway:5000';

app.get('/', (_req,res)=>res.send('API up'));
app.get('/config', (_req,res)=>res.json({ BASE_PRICE, COUPON_CODE, DISCOUNT_PCT, BUG_MODE }));

app.get('/gateway/charges', async (_req,res)=>{
  try{
    const r = await fetch(`${GATEWAY_URL}/charges`);
    res.json(await r.json());
  }catch(e){
    res.status(500).json({ error:'Failed to fetch gateway charges', details:String(e) });
  }
});

app.post('/pay', async (req,res)=>{
  const { coupon } = req.body || {};
  const isValid = coupon === COUPON_CODE;
  const discounted = isValid ? Math.round(BASE_PRICE * (1 - DISCOUNT_PCT) * 100)/100 : BASE_PRICE;

  const amountToCharge = BUG_MODE ? BASE_PRICE : discounted; // <-- BUG

  try{
    const r = await fetch(`${GATEWAY_URL}/charge`, {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ amount: amountToCharge, currency:'USD', reference:`order_${Date.now()}` })
    });
    const j = await r.json();
    return res.json({
      ok:true,
      expectedClientPrice: discounted,
      chargedViaGateway: j?.charge?.amount ?? amountToCharge,
      bugMode: BUG_MODE
    });
  }catch(e){
    return res.status(502).json({ ok:false, error:'Gateway charge failed', details:String(e) });
  }
});

app.listen(PORT, ()=>console.log('API listening on :' + PORT));
