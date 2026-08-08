from fastapi import APIRouter, Depends
from decimal import Decimal
from app.auth.dependencies import get_current_user
from app.services.currency_service import CurrencyService

router = APIRouter()

@router.get("/rate")
async def get_rate(from_currency: str, to_currency: str, current_user = Depends(get_current_user)):
    rate = await CurrencyService.get_exchange_rate(from_currency, to_currency)
    return {"from": from_currency, "to": to_currency, "rate": float(rate) if rate else None}

@router.get("/convert")
async def convert_currency(amount: Decimal, from_currency: str, to_currency: str, current_user = Depends(get_current_user)):
    result = await CurrencyService.convert(amount, from_currency, to_currency)
    return {"amount": float(amount), "from": from_currency, "to": to_currency, "converted": float(result) if result else None}

@router.get("/currencies")
async def get_currencies(current_user = Depends(get_current_user)):
    return await CurrencyService.get_supported_currencies()
