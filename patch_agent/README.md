# 💳 SecurePay Gateway - Professional Payment Processing

A modern, professional payment gateway application that demonstrates secure payment processing with a beautiful, responsive user interface. This application showcases payment processing bugs and their fixes in a realistic payment gateway environment.

## ✨ Features

- 🎨 **Modern UI/UX**: Professional payment gateway interface with responsive design
- 💳 **Secure Payments**: Integrated payment processing with coupon support
- 🔄 **Real-time Updates**: Live transaction history and status updates
- 🐛 **Bug Mode Demo**: Demonstrates payment processing bugs and fixes
- 📱 **Mobile Responsive**: Optimized for all device sizes
- 🔒 **Security Badges**: SSL and PCI compliance indicators

## 🏗️ Architecture

- **Frontend**: React with Vite, modern CSS styling
- **API**: Node.js Express server (contains the payment bug)
- **Gateway**: Payment processing service with transaction ledger
- **Containerization**: Docker Compose for easy deployment

## 🚀 Quick Start

```bash
docker-compose up --build
```

**Access Points:**
- 🌐 **Web Interface**: http://localhost:5173
- 🔌 **API**: http://localhost:4000
- 💳 **Gateway**: http://localhost:5000

## 🎯 Demo Scenario

**The Bug:** Coupon `FIXME50` applies a 50% discount to a $100 item. The frontend shows $50.00, but a backend bug charges the payment gateway $100.00.

### How to Demo:
1. Open **http://localhost:5173**
2. Coupon is prefilled `FIXME50` → UI shows **Final: $50.00**
3. Click **Pay**
4. UI displays: Expected $50.00 | Gateway charged **$100.00** (BUG)

### To Fix the Bug:
Set `BUG_MODE=false` in docker-compose environment variables, rebuild, and re-run. Then the gateway charges the correct $50.00.

## 🛠️ Development

### With Docker (Recommended)
```bash
docker-compose up --build
```

### Local Development
```bash
# API
cd api && npm i && npm run dev

# Gateway  
cd gateway && npm i && npm run dev

# Web (new terminal)
cd web && npm i && npm run dev
```

## 🎨 UI Improvements

The application now features:
- Professional payment gateway design
- Responsive layout for all devices
- Modern CSS with gradients and animations
- Real-time status indicators
- Transaction history with detailed cards
- Security badges and compliance indicators
- Loading states and smooth transitions

## 🔧 Configuration

Environment variables can be set in `docker-compose.yml`:
- `BUG_MODE`: Enable/disable the payment bug
- `BASE_PRICE`: Set the base item price
- `DISCOUNT_PCT`: Set the discount percentage
- `COUPON_CODE`: Set the valid coupon code
