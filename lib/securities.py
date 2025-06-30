
import requests
from config.config import SECUTIRY_URL, TOKEN_BLUEPILL

def get_active_securities_isin() -> list[str]:
    HEADERS = {
        'Authorization': TOKEN_BLUEPILL,
        'content-type':'application/json',
    }
    try:
        print(SECUTIRY_URL)
        r = requests.get(url=SECUTIRY_URL, headers=HEADERS)
        if r.status_code != 200:
            raise Exception(f"Error fetching securities: {r.status_code} - {r.text}")

        data = r.json()
        results = data.get("results", [])
        filter_result = list(filter(lambda security: security["cob_market_status"] == "open"\
                                    and security.get("security_type") == "m-bono", results))
        return list(map(lambda security:  security.get("isin", ""), filter_result))

    except Exception as e:
        print(e)
        return []
