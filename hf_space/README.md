---
title: Customer Loyalty Points Engine
emoji: 🎁
colorFrom: purple
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# Customer Loyalty Points Engine

Earn, redeem, and track loyalty points with Bronze/Silver/Gold tier multipliers.

The landing page is an interactive API console — click any endpoint to call the live API.

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/customers` | List customers |
| POST | `/api/earn` | Earn points for an order |
| POST | `/api/redeem` | Redeem points |
| GET | `/api/customer/{id}/balance` | Points balance + tier |

## Stack

Python 3.11 · FastAPI · SQLite · Pydantic v2 · Next.js 14 (static export) · Tailwind CSS · Docker
