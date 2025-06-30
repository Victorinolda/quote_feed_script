

import json
import time
from typing import List, TypedDict

import requests
from config.config import HEADERS, URL_PLUTUS,SLEEP_TIME_POST_QUOTE_FEED


class QuoteFeed(TypedDict):
    isin: str
    data_type: str
    value: float
    quote_feed_id: str
    timestamp: str
    
class QuoteFeedFactory:
    @staticmethod
    def create(isin: str, data_type: str, value: float, quote_feed_id: str, timestamp: str) -> QuoteFeed:
        return {
            "isin": isin,
            "data_type": data_type,
            "value": value,
            "quote_feed_id": quote_feed_id,
            "timestamp": timestamp
        }

    @staticmethod
    def bulk_create(isin: str, data_type: str, values: List[float], quote_feed_id: str, timestamp: str) -> List[QuoteFeed]:
        quote_feeds:List[QuoteFeed] = []

        for value in values:
            quote_feed = QuoteFeedFactory.create(
                isin=isin,
                data_type=data_type,
                value=value,
                quote_feed_id=quote_feed_id,
                timestamp=timestamp
            )
            quote_feeds.append(quote_feed)

        return quote_feeds


def post_quote_feed(payload:QuoteFeed):
    try:
        data_as_json = json.dumps(payload)
        time.sleep(SLEEP_TIME_POST_QUOTE_FEED) 
        r =  requests.post(url=URL_PLUTUS, data=data_as_json, headers=HEADERS)
        if r.status_code < 200 or r.status_code >= 300:
            raise Exception(f"Failed to post quote feed: {r.text}")
        print(f"Processing single stream for {payload['isin']} with yield: {payload['value']}, direction: {payload['data_type']}")
    except Exception as e:
        print(e)

def post_quote_feed_bulk(payloads: List[QuoteFeed]):
    try:
        for payload in payloads:
            post_quote_feed(payload)
    except Exception as e:
        print(e)


