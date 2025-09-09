from random import shuffle
import time
from typing import Dict, List 
from config.config import QUOTE_ID, TIMESTAMP
from lib.quoute_feed import QuoteFeed, QuoteFeedFactory, post_quote_feed, post_quote_feed_bulk
from lib.securities import get_active_securities_isin
from lib.utilies import generate_array_yield

import concurrent.futures


def process_multiple_streams(yield_value: float = 10.0):
    print(f"yield_value: {yield_value}")
    securities = get_active_securities_isin()
    if not securities:
        print("No active securities found.")
        return

    print(f"Found {len(securities)} active securities: {securities}")

    NUM_THREADS = len(securities)

    ask_yield_values = generate_array_yield(base_yield=yield_value, direction="ask")
    bid_yield_values = generate_array_yield(base_yield=yield_value, direction="bid")


    payloads_by_isin:Dict[str,List[QuoteFeed]] = {}

    for isin in securities:
        bid_payloads = QuoteFeedFactory.bulk_create(
            isin=isin,
            data_type="bid",
            values=bid_yield_values,
            quote_feed_id=QUOTE_ID,
            timestamp=TIMESTAMP
        )
        ask_payloads = QuoteFeedFactory.bulk_create(
            isin=isin,
            data_type="ask",
            values=ask_yield_values,
            quote_feed_id=QUOTE_ID,
            timestamp=TIMESTAMP
        )
        payloads_by_isin[isin] = {
            "bid": bid_payloads,
            "ask": ask_payloads
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        threads = []
        for isin, payloads in payloads_by_isin.items():
            threads.append(executor.submit(post_quote_feed_bulk, payloads, True))




