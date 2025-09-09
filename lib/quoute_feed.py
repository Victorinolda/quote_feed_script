

import json
import time
from types import new_class
from typing import List, TypedDict

import requests
from config.config import HEADERS, URL_PLUTUS,SLEEP_TIME_POST_QUOTE_FEED
from lib.utilies import new_time_stamp


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
                timestamp=new_time_stamp()
            )
            quote_feeds.append(quote_feed)

        return quote_feeds


def post_quote_feed(payload:QuoteFeed, is_bulk: bool = False):
    try:
        data_as_json = json.dumps(payload)
        if not is_bulk:
            time.sleep(SLEEP_TIME_POST_QUOTE_FEED) 
        # print(URL_PLUTUS, data_as_json, HEADERS)
        r =  requests.post(url=URL_PLUTUS, data=data_as_json, headers=HEADERS)
        print(r.text)
        if r.status_code < 200 or r.status_code >= 300:
            raise Exception(f"Failed to post quote feed: {r.text}")
        print(f"Processing single stream for {payload['isin']} with yield: {payload['value']}, direction: {payload['data_type']}")
    except Exception as e:
        print(e)

def post_quote_feed_bulk(payloads: List[QuoteFeed], is_bulk: bool = False):
    try:
        bids = payloads.get("bid", [])
        asks = payloads.get("ask", [])

        for i in range(len(bids)):

            post_quote_feed(bids[i], is_bulk)
            post_quote_feed(asks[i], is_bulk)
            if is_bulk:
                time.sleep(SLEEP_TIME_POST_QUOTE_FEED)
    except Exception as e:
        print(e)


