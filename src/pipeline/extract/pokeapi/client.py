import json
import logging
import time
import urllib.request
import urllib.error
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class PokeAPIClient:
    """Simple robust HTTP client to fetch data from PokeAPI with retries, exponential backoff, and rate limiting."""
    
    def __init__(self, base_url: str = "https://pokeapi.co/api/v2/", delay_between_requests: float = 0.2):
        self.base_url = base_url
        self.delay_between_requests = delay_between_requests
        self.last_request_time = 0.0

    def get(self, endpoint: str) -> Dict[str, Any]:
        """Fetch json from endpoint, with retries on transit errors and rate limiting."""
        # Enforce rate limiting delay
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay_between_requests:
            sleep_time = self.delay_between_requests - elapsed
            time.sleep(sleep_time)

        url = endpoint if endpoint.startswith("http") else f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        retries = 5
        backoff = 1.0
        
        while retries > 0:
            try:
                self.last_request_time = time.time()
                req = urllib.request.Request(url, headers={"User-Agent": "PokemonCompanionExtractor/1.0"})
                with urllib.request.urlopen(req, timeout=15) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    logger.warning(f"Resource not found (404) at {url}")
                    raise
                if e.code in [429, 500, 502, 503, 504] and retries > 1:
                    retries -= 1
                    logger.warning(f"HTTP error {e.code} fetching {url}. Retrying in {backoff}s...")
                    time.sleep(backoff)
                    backoff *= 2
                else:
                    logger.error(f"HTTP error {e.code} fetching {url}: {e.reason}")
                    raise
            except Exception as e:
                if retries > 1:
                    retries -= 1
                    logger.warning(f"Network/Timeout error fetching {url}: {str(e)}. Retrying in {backoff}s...")
                    time.sleep(backoff)
                    backoff *= 2
                else:
                    logger.error(f"Error fetching {url}: {str(e)}")
                    raise
        raise Exception(f"Failed to fetch {url} after multiple retries")

    def get_list(self, resource: str, limit: int = 150) -> List[Dict[str, Any]]:
        """Retrieve the flat list of references (name & url) for a specific resource type."""
        logger.info(f"Retrieving list of {resource} with page limit {limit}...")
        results = []
        url = f"{self.base_url.rstrip('/')}/{resource.lstrip('/')}?limit={limit}"
        while url and len(results) < limit:
            data = self.get(url)
            results.extend(data.get("results", []))
            url = data.get("next")
        logger.info(f"Found {len(results)} items for {resource}")
        return results[:limit]
