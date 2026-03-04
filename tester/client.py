import requests
import time

class APIClient:
    def __init__(self, base_url, timeout=3, retries=1):
        self.base_url = base_url
        self.timeout = timeout
        self.retries = retries

    def get(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        attempt = 0

        while attempt <= self.retries:
            start = time.time()
            try:
                response = requests.get(url, timeout=self.timeout)
                latency = time.time() - start

                # Gestion 429 (trop de requêtes)
                if response.status_code == 429:
                    time.sleep(1)
                    attempt += 1
                    continue

                # Gestion erreurs 5xx
                if 500 <= response.status_code < 600:
                    attempt += 1
                    continue

                return response, latency

            except requests.exceptions.Timeout:
                attempt += 1

        return None, None
