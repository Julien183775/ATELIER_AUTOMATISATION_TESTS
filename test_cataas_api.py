import time
import requests
import pytest

BASE_URL = "https://cataas.com"
TIMEOUT = 10
MAX_RETRIES = 3
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}


class ApiCallError(Exception):
    """Erreur levée quand l'API échoue après plusieurs tentatives."""


def call_api(
    path: str,
    method: str = "GET",
    params: dict | None = None,
    headers: dict | None = None,
    expected_status: int = 200,
):
    """
    Appelle l'API avec timeout + retry simple.
    - retry sur erreurs réseau
    - retry sur 429 et 5xx
    - lève une erreur claire si toutes les tentatives échouent
    """
    url = f"{BASE_URL}{path}"
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                timeout=TIMEOUT,
            )

            # Retry simple sur erreurs temporaires
            if response.status_code in RETRY_STATUS_CODES:
                last_error = ApiCallError(
                    f"Statut temporaire {response.status_code} sur {url}"
                )
                if attempt < MAX_RETRIES:
                    time.sleep(attempt)  # backoff simple : 1s, 2s, 3s
                    continue

            # Vérification du code attendu
            if response.status_code != expected_status:
                raise AssertionError(
                    f"Statut inattendu pour {url}: "
                    f"attendu={expected_status}, obtenu={response.status_code}"
                )

            return response

        except requests.Timeout as exc:
            last_error = ApiCallError(f"Timeout sur {url}") from exc
            if attempt < MAX_RETRIES:
                time.sleep(attempt)
                continue

        except requests.RequestException as exc:
            last_error = ApiCallError(f"Erreur réseau sur {url}: {exc}") from exc
            if attempt < MAX_RETRIES:
                time.sleep(attempt)
                continue

    raise last_error if last_error else ApiCallError(f"Échec appel API sur {url}")


def test_random_cat_returns_image():
    response = call_api("/cat")
    assert response.headers["Content-Type"].startswith("image/")


def test_cat_says_returns_image():
    response = call_api("/cat/says/Bonjour")
    assert response.headers["Content-Type"].startswith("image/")


def test_random_cat_json_format():
    response = call_api(
        "/cat",
        params={"json": "true"},
        headers={"Accept": "application/json"},
    )

    assert response.headers["Content-Type"].startswith("application/json")
    data = response.json()

    assert isinstance(data, dict)
    assert len(data) > 0


def test_tags_returns_json_array():
    response = call_api("/api/tags")
    assert response.headers["Content-Type"].startswith("application/json")

    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        assert isinstance(data[0], str)


def test_cats_search_with_params():
    response = call_api(
        "/api/cats",
        params={"tags": "cute", "skip": 0, "limit": 5},
    )
    assert response.headers["Content-Type"].startswith("application/json")

    data = response.json()
    assert isinstance(data, list)


def test_invalid_route_returns_404():
    response = call_api(
        "/route-inexistante-xyz",
        expected_status=404,
    )
    assert response.status_code == 404


def test_cat_with_text_and_color():
    response = call_api(
        "/cat/says/Hello",
        params={"color": "red", "size": 50},
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("image/")
