import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.GATEWAY_PORT ? Number(process.env.GATEWAY_PORT) : 5000;
const charges = [];

app.get('/', (_req,res)=>res.send('Payment Gateway up'));
app.get('/charges', (_req,res)=>res.json({ count: charges.length, charges }));

app.post('/charge', (req,res)=>{
  const { amount, currency='USD', reference } = req.body || {};
  const record = { id:'ch_'+Date.now(), amount:Number(amount), currency, reference: reference||'N/A', ts:new Date().toISOString() };
  charges.push(record);
  console.log('[GATEWAY] CHARGE', record);
  res.json({ ok:true, charge: record });
});

app.listen(PORT, ()=>console.log('Gateway listening on :' + PORT));
