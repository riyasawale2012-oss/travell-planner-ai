import httpx
from decimal import Decimal
from typing import Optional
from app.config import settings

class CurrencyService:
    @staticmethod
    async def get_exchange_rate(from_currency: str, to_currency: str) -> Optional[Decimal]:
        if not settings.EXCHANGE_API_KEY:
            rates = {
                ("INR", "USD"): Decimal("0.012"), ("USD", "INR"): Decimal("83.5"),
                ("INR", "EUR"): Decimal("0.011"), ("EUR", "INR"): Decimal("90.2"),
                ("INR", "GBP"): Decimal("0.0094"), ("GBP", "INR"): Decimal("106.3"),
                ("INR", "THB"): Decimal("0.41"), ("THB", "INR"): Decimal("2.44"),
                ("INR", "AED"): Decimal("0.044"), ("AED", "INR"): Decimal("22.7"),
            }
            return rates.get((from_currency.upper(), to_currency.upper()), Decimal("1"))
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://v6.exchangerate-api.com/v6/{settings.EXCHANGE_API_KEY}/pair/{from_currency}/{to_currency}")
            if response.status_code == 200:
                data = response.json()
                return Decimal(str(data.get("conversion_rate", 1)))
            return None

    @staticmethod
    async def convert(amount: Decimal, from_currency: str, to_currency: str) -> Optional[Decimal]:
        rate = await CurrencyService.get_exchange_rate(from_currency, to_currency)
        return amount * rate if rate else None

    @staticmethod
    async def get_supported_currencies() -> list:
        return [
            {"code": "INR", "name": "Indian Rupee", "symbol": "₹"},
            {"code": "USD", "name": "US Dollar", "symbol": "$"},
            {"code": "EUR", "name": "Euro", "symbol": "€"},
            {"code": "GBP", "name": "British Pound", "symbol": "£"},
            {"code": "AED", "name": "UAE Dirham", "symbol": "د.إ"},
            {"code": "THB", "name": "Thai Baht", "symbol": "฿"},
            {"code": "SGD", "name": "Singapore Dollar", "symbol": "S$"},
            {"code": "JPY", "name": "Japanese Yen", "symbol": "¥"},
        ]
