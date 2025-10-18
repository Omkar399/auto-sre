import React, { useMemo, useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_BASE || 'http://localhost:4000';

export default function App(){
  const [coupon, setCoupon] = useState('FIXME50');
  const [config, setConfig] = useState({ BASE_PRICE: 100, DISCOUNT_PCT: 0.5, BUG_MODE: true });
  const [status, setStatus] = useState('');
  const [lastCharge, setLastCharge] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(()=>{
    fetch(API + '/config').then(r=>r.json()).then(setConfig).catch(()=>{});
    refreshCharges();
  },[]);

  const discounted = useMemo(()=>{
    const base = Number(config.BASE_PRICE||100);
    const pct  = Number(config.DISCOUNT_PCT||0.5);
    const ok = coupon === 'FIXME50';
    return ok ? (base * (1 - pct)) : base;
  },[config, coupon]);
  const finalPrice = (Math.round(discounted * 100) / 100).toFixed(2);

  async function refreshCharges(){
    try{
      const r = await fetch(API + '/gateway/charges');
      const j = await r.json();
      setLastCharge(j?.charges?.slice(-1)[0] || null);
    }catch(e){ /* ignore */ }
  }

  async function pay(){
    setIsLoading(true);
    setStatus('Processing payment...');
    try{
      const r = await fetch(API + '/pay', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ coupon })
      });
      const j = await r.json();
      if(!r.ok) throw new Error(j?.error || 'Payment error');
      await refreshCharges();
      setStatus(`✅ Payment Success. Expected: $${Number(j.expectedClientPrice).toFixed(2)} | Gateway charged: $${Number(j.chargedViaGateway).toFixed(2)} ${j.bugMode?'(BUG)':'(FIXED)'}`);
    }catch(e){
      setStatus('❌ ' + e.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <div className="logo">
            <div className="logo-icon">💳</div>
            <h1>SecurePay Gateway</h1>
          </div>
          <div className="status-indicator">
            <div className={`status-dot ${config.BUG_MODE ? 'bug' : 'fixed'}`}></div>
            <span>{config.BUG_MODE ? 'Bug Mode' : 'Fixed Mode'}</span>
          </div>
        </header>

        <main className="main-content">
          <div className="payment-card">
            <div className="payment-header">
              <h2>Complete Your Payment</h2>
              <p className="payment-subtitle">Secure payment processing powered by SecurePay</p>
            </div>

            <div className="price-section">
              <div className="price-row">
                <span className="price-label">Base Price:</span>
                <span className="price-value">${Number(config.BASE_PRICE).toFixed(2)}</span>
              </div>
              {coupon === 'FIXME50' && (
                <div className="discount-row">
                  <span className="discount-label">Discount (50%):</span>
                  <span className="discount-value">-${(Number(config.BASE_PRICE) * 0.5).toFixed(2)}</span>
                </div>
              )}
              <div className="total-row">
                <span className="total-label">Total:</span>
                <span className="total-value">${finalPrice}</span>
              </div>
            </div>

            <div className="coupon-section">
              <label htmlFor="coupon" className="coupon-label">Coupon Code</label>
              <div className="coupon-input-group">
                <input 
                  id="coupon"
                  type="text" 
                  value={coupon} 
                  onChange={e=>setCoupon(e.target.value)} 
                  className="coupon-input"
                  placeholder="Enter coupon code"
                />
                {coupon === 'FIXME50' && (
                  <span className="coupon-badge">Valid</span>
                )}
              </div>
            </div>

            <button 
              onClick={pay} 
              disabled={isLoading}
              className={`pay-button ${isLoading ? 'loading' : ''}`}
            >
              {isLoading ? (
                <>
                  <div className="spinner"></div>
                  Processing...
                </>
              ) : (
                <>
                  <span>Pay ${finalPrice}</span>
                  <span className="button-icon">→</span>
                </>
              )}
            </button>

            {status && (
              <div className={`status-message ${status.includes('✅') ? 'success' : 'error'}`}>
                {status}
              </div>
            )}
          </div>

          <div className="transaction-history">
            <h3>Transaction History</h3>
            {lastCharge ? (
              <div className="transaction-card">
                <div className="transaction-header">
                  <span className="transaction-amount">${Number(lastCharge.amount).toFixed(2)} {lastCharge.currency}</span>
                  <span className="transaction-status success">Completed</span>
                </div>
                <div className="transaction-details">
                  <div className="transaction-ref">
                    <span className="label">Reference:</span>
                    <span className="value">{lastCharge.reference}</span>
                  </div>
                  <div className="transaction-time">
                    <span className="label">Time:</span>
                    <span className="value">{new Date(lastCharge.ts).toLocaleString()}</span>
                  </div>
                </div>
              </div>
            ) : (
              <div className="no-transactions">
                <div className="no-transactions-icon">📋</div>
                <p>No transactions yet</p>
                <small>Complete a payment to see transaction history</small>
              </div>
            )}
          </div>
        </main>

        <footer className="footer">
          <div className="footer-content">
            <div className="system-info">
              <p>
                <strong>System Status:</strong> {config.BUG_MODE ? 'Bug Mode Active' : 'Fixed Mode Active'}
              </p>
              <p>
                <strong>API Endpoint:</strong> {API}
              </p>
            </div>
            <div className="security-badges">
              <span className="security-badge">🔒 SSL Secured</span>
              <span className="security-badge">🛡️ PCI Compliant</span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
