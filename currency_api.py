import requests


class CurrencyAPI:
    def __init__(self):
        self.url = "https://api.api-ninjas.com/v1/convertcurrency"

    def get_rates(self):
        try:
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()

            data = response.json()

            kzt = data["rates"]["KZT"]
            eur = data["rates"]["EUR"]

            return {
                "USD_KZT": round(kzt, 2),
                "EUR_KZT": round(kzt / eur, 2)
            }

        except requests.RequestException:
            return None
        except KeyError:
            return None
        except Exception:
            return None