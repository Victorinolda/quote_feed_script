
from lib.quoute_feed import QuoteFeedFactory, post_quote_feed
from lib.utilies import generate_array_yield, countdown

from config.config import ISIN, QUOTE_ID, NUMBER_OF_QUOTES, TIMESTAMP

def process_single_stream(yield_value: float , direction: str = "bid"):
    if direction not in ["bid", "ask", "both"]:
        raise ValueError("Direction must be either 'bid' or 'ask'.")
    if NUMBER_OF_QUOTES <= 0:
        raise ValueError("Number of iterations must be greater than 0.")

    
    countdown(3)

    payloads = []

    if direction == "both":
        bid_values = generate_array_yield(yield_value, NUMBER_OF_QUOTES, "bid")
        bid_payloads = QuoteFeedFactory.bulk_create(
            isin=ISIN,
            data_type="bid",
            values=bid_values,
            quote_feed_id=QUOTE_ID,
        )
        ask_values = generate_array_yield(yield_value, NUMBER_OF_QUOTES, "ask")
        ask_payloads = QuoteFeedFactory.bulk_create(
            isin=ISIN,
            data_type="ask",
            values=ask_values,
            quote_feed_id=QUOTE_ID,
        )
        payloads = bid_payloads + ask_payloads
    else:
        range_yield_values = generate_array_yield(yield_value, NUMBER_OF_QUOTES, direction)
        payloads = QuoteFeedFactory.bulk_create(
            isin=ISIN,
            data_type=direction,
            values=range_yield_values,
            quote_feed_id=QUOTE_ID,
        )


    for payload in payloads:
        if payload["value"] < 0:
            print(f"Yield value {payload['value']} is negative, skipping.")
            continue
        post_quote_feed(payload)

    
