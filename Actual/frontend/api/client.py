import requests

from config import (
    API_BASE_URL,
    PREDICTION_ENDPOINT,
    RECOMMENDATION_ENDPOINT,
    EXPLAINABILITY_ENDPOINT,
    REQUEST_TIMEOUT,
    VERIFY_SSL
)


# =====================================================
# API CLIENT
# =====================================================

class APIClient:

    def __init__(self):
        self.timeout = REQUEST_TIMEOUT
        self.verify = VERIFY_SSL

    # =================================================
    # INTERNAL REQUEST METHODS
    # =================================================

    def _post(self, url, payload=None):

        try:

            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout,
                verify=self.verify
            )

            response.raise_for_status()

            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json()
            }

        except requests.exceptions.HTTPError as e:

            try:
                error = response.json()
            except Exception:
                error = str(e)

            return {
                "success": False,
                "status_code": response.status_code,
                "error": error
            }

        except requests.exceptions.ConnectionError:

            return {
                "success": False,
                "status_code": None,
                "error": "Couldn't connect right now. Please try again in a moment."
            }

        except requests.exceptions.Timeout:

            return {
                "success": False,
                "status_code": None,
                "error": "This is taking longer than expected. Please try again."
            }

        except Exception as e:

            return {
                "success": False,
                "status_code": None,
                "error": str(e)
            }

    # =================================================
    # PREDICTION
    # =================================================

    def predict(self, laptop_information):

        return self._post(
            PREDICTION_ENDPOINT,
            laptop_information
        )

    # =================================================
    # RECOMMENDATION
    # =================================================

    def recommend(self, prediction_id):

        url = f"{RECOMMENDATION_ENDPOINT}/{prediction_id}"

        return self._post(url)

    # =================================================
    # EXPLAINABILITY
    # =================================================

    def explain(self, prediction_id):

        url = f"{EXPLAINABILITY_ENDPOINT}/{prediction_id}"

        return self._post(url)

    # =================================================
    # HEALTH CHECK
    # =================================================

    def health_check(self):

        # Try a couple of likely endpoints so this doesn't silently
        # report "down" just because /docs happens to be disabled.
        for path in ("/health", "/", "/docs"):

            try:

                response = requests.get(
                    f"{API_BASE_URL}{path}",
                    timeout=5,
                    verify=self.verify
                )

                if response.status_code < 500:
                    return True

            except Exception:
                continue

        return False


# =====================================================
# SINGLETON
# =====================================================

api_client = APIClient()


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def predict(laptop_information):
    return api_client.predict(laptop_information)


def recommend(prediction_id):
    return api_client.recommend(prediction_id)


def explain(prediction_id):
    return api_client.explain(prediction_id)


def backend_available():
    return api_client.health_check()
