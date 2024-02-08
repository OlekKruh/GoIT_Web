import asyncio
import aiohttp
import requests
from datetime import datetime, timedelta

CURRENCY_LIST = {
    'USD': 'USD',
    '1': 'USD',
    'EUR': 'EUR',
    '2': 'EUR',
    'CHF': 'CHF',
    '3': 'CHF',
    'GBP': 'GBP',
    '4': 'GBP',
    'PLZ': 'PLZ',
    '5': 'PLZ',
    'SEK': 'SEK',
    '6': 'SEK',
    'XAU': 'XAU',
    '7': 'XAU',
    'CAD': 'CAD',
    '8': 'CAD',
}


def communication():
    print(f'1. USD\n'
          f'2. EUR\n'
          f'3. CHF\n'
          f'4. GBP\n'
          f'5. PLZ\n'
          f'6. SEK\n'
          f'7. XAU\n'
          f'8. CAD\n')
    user_currency_input = input(f'What exchange rate are you interested in?\n'
                                f'>>> ').lower()

    for currency_key, currency_value in CURRENCY_LIST.items():
        if user_currency_input == currency_key.lower():
            try:
                user_days_input = int(input(f'How many days from the archive do you want to see?\n'
                                            f'>>> '))
                return currency_value, user_days_input
            except ValueError:
                print(f'Error: incorrect value input. Try again.')
                return None

    print('Error: Incorrect currency input. Try again.')
    return None


async def get_exchange_rate(currency, days):
    today_data = datetime.now()
    url = 'https://api.privatbank.ua/p24api/exchange_rates?date='

    async with aiohttp.ClientSession() as session:
        try:
            for i in range(days, 0, -1):
                archive_day = today_data - timedelta(days=i)
                formatted_archive_day = archive_day.strftime("%d.%m.%Y")
                question_url = url + formatted_archive_day

                async with session.get(question_url) as response:
                    response.raise_for_status()
                    data = await response.json()

                    for rate in data.get("exchangeRate", []):
                        if rate.get("currency") == currency:
                            print(f"Exchange rate for {currency} on {formatted_archive_day}:")
                            print(f"Purchase Rate: {rate.get('purchaseRateNB')}")
                            print(f"Sale Rate: {rate.get('saleRateNB')}")
                            break
                    else:
                        print(f"No data found for {currency} on {formatted_archive_day}")

        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")


async def main():
    currency_value, user_days_input = communication()

    try:
        if currency_value and user_days_input:
            await get_exchange_rate(currency_value, user_days_input)
    except Exception as e:
        print(f"An error occurred in the main function: {e}")


if __name__ == "__main__":
    asyncio.run(main())
