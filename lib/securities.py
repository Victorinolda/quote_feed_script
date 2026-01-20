from enum import Enum
from typing import TypedDict
import requests
from config.config import SECUTIRY_URL, TOKEN_BLUEPILL


class SecurityType(Enum):
    M_BONO = "m-bono"


class ISecurity(TypedDict):
    isin: str
    cob_market_status: str
    security_type: str
    id: str


class Security(ISecurity):
    def __init__(self, isin: str, cob_market_status: str, security_type: str, id: str):
        self.isin = isin
        self.cob_market_status = cob_market_status
        self.security_type = security_type
        self.id = id


def get_active_securities_isin() -> list[str]:
    HEADERS = {
        "Authorization": TOKEN_BLUEPILL,
        "content-type": "application/json",
    }
    try:
        print(SECUTIRY_URL)
        r = requests.get(url=SECUTIRY_URL, headers=HEADERS)
        if r.status_code != 200:
            raise Exception(f"Error fetching securities: {r.status_code} - {r.text}")

        data = r.json()
        results = data.get("results", [])
        filter_result = list(
            filter(
                lambda security: security["cob_market_status"] == "open"
                and security.get("security_type") == "m-bono",
                results,
            )
        )
        return list(map(lambda security: security.get("isin", ""), filter_result))

    except Exception as e:
        print(e)
        return []


def get_active_securitie_by_type(securityType: SecurityType | None) -> list[ISecurity]:
    HEADERS = {
        "Authorization": TOKEN_BLUEPILL,
        "content-type": "application/json",
    }
    if securityType is None:
        securityType = SecurityType.M_BONO

    try:
        print(SECUTIRY_URL)
        r = requests.get(url=SECUTIRY_URL, headers=HEADERS)
        if r.status_code != 200:
            raise Exception(f"Error fetching securities: {r.status_code} - {r.text}")

        data = r.json()
        results = data.get("results", [])
        filter_result = list(
            filter(
                lambda security: security["cob_market_status"] == "open"
                and security.get("security_type") == "m-bono",
                results,
            )
        )
        securities: list[ISecurity] = []
        for security in filter_result:
            sec = Security(
                isin=security.get("isin", ""),
                cob_market_status=security.get("cob_market_status", ""),
                security_type=security.get("security_type", ""),
                id=security.get("id", ""),
            )
            securities.append(sec)
        return securities

    except Exception as e:
        print(e)
        return []
