from enum import Enum
import json
from typing import Dict, TypedDict

import requests
from config.config import BLUEPILL_HOST, TOKEN_BLUEPILL


class OrderType(Enum):
    LIMIT = "limit"
    MARKET = "market"
    IOC = "ioc"


class OrderDirection(Enum):
    BID = "bid"
    ASK = "ask"


class OrdersPayload(TypedDict):
    direction: OrderDirection
    expiration: str
    order_type: OrderType
    quantity: str
    security_id: str
    yield_value: str


class OrderPayloadJson(TypedDict):
    direction: str
    expiration: str
    order_type: str
    quantity: str
    security_id: str
    yield_value: str


class OrdersPayloadFactory:
    @staticmethod
    def create(
        direction: OrderDirection,
        expiration: str,
        order_type: OrderType,
        quantity: str,
        security_id: str,
        yield_value: str,
    ) -> OrderPayloadJson:
        return {
            "direction": direction.value,
            "expiration": expiration,
            "order_type": order_type.value,
            "quantity": quantity,
            "security_id": security_id,
            "yield_value": yield_value,
        }

    @staticmethod
    def bulk_create_same_direction(
        direction: OrderDirection,
        expiration: str,
        order_type: OrderType,
        quantity: str,
        security_ids: list[str],
        yield_values: list[str],
    ) -> list[OrderPayloadJson]:
        orders_payloads: list[OrderPayloadJson] = []

        for security_id, yield_value in zip(security_ids, yield_values):
            order_payload = OrdersPayloadFactory.create(
                direction=direction,
                expiration=expiration,
                order_type=order_type,
                quantity=quantity,
                security_id=security_id,
                yield_value=yield_value,
            )
            orders_payloads.append(order_payload)

        return orders_payloads


def create_order(payload: OrderPayloadJson):
    try:
        # stringify the payload
        data_as_json = json.dumps(payload)
        # try to post the order to bluepill (note we are using the url used in curve scanner)
        url = f"{BLUEPILL_HOST}/api/v0/market/place-holder-id/cob-order/"
        headers = {
            "Content-Type": "application/json",
            "Authorization": TOKEN_BLUEPILL,
        }
        r = requests.post(url=url, data=data_as_json, headers=headers)
        if r.status_code < 200 or r.status_code >= 300:
            raise Exception(f"Failed to create order: {r.text}")

        print(f"Order created successfully: {r.text}")
    except Exception as e:
        print(e)
