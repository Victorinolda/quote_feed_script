import random
from typing import Dict
import time
import json
from lib.orders import OrdersPayloadFactory, OrderDirection, OrderType, create_order

from config.config import QUOTE_ID, SLEEP_TIME_POST_QUOTE_FEED, ENV
from lib.securities import (
    ISecurity,
    SecurityType,
    get_active_securitie_by_type,
)


class CreateBulkOrders:
    securities: list[str] = []
    quote_id: str
    market_dict: Dict[str, Dict[str, float]] = {}
    last_security: str | None
    base_yield: float = 11.0
    orders_direction: list[OrderDirection] = [OrderDirection.BID, OrderDirection.ASK]
    base_point: float = 0.01
    _file_path: str
    default_diff: float = 0.1
    debug: bool = False
    time_sleep: float

    import threading

    _lock = threading.Lock()

    def __init__(self, quote_id: str, time_sleep: float, debug: bool = False):
        self.quote_id = quote_id
        self.time_sleep = time_sleep
        self.last_security = None
        self._file_path = self.__file_path()
        self.debug = debug
        # Maximum number of concurrent workers (adjust as needed)
        self.max_workers = 10

    def __file_path(self) -> str:
        env_suffix = "" if ENV == "local" else f"_{ENV}"
        return f"create_bulk_state{env_suffix}.json"

    def generate_initial_market_dict(self):
        market_dict: Dict[str, Dict[str, float]] = dict()
        for security in self.securities:
            yield_ask_value = self.base_yield - self.base_point - self.default_diff
            yield_bid_value = self.base_yield + self.base_point
            market_dict[security] = {
                "ask": yield_ask_value,
                "bid": yield_bid_value,
            }
        self.market_dict = market_dict

    def get_securities(self):
        # Example securities list; replace with actual securities retrieval logic
        if self.debug:
            self.securities = ["1"]
            return
        securities_active: list[ISecurity] = get_active_securitie_by_type(
            SecurityType.M_BONO
        )
        securities_ids: list[str] = []
        for security in securities_active:
            securities_ids.append(security["id"])
        self.securities = securities_ids

    def initialize_market(self):
        self.get_securities()
        if not self.securities:
            print("No active securities found.")
            return
        self.generate_initial_market_dict()

    def _save_state(self):
        with open(self._file_path, "w") as f:
            json.dump(self.market_dict, f)

    def _load_state(self):
        try:
            with open(self._file_path, "r") as f:
                print("Loading saved state...")
                self.market_dict = json.load(f)
                self.securities = list(self.market_dict.keys())
        except FileNotFoundError:
            print("No saved state found, starting fresh.")
            self.initialize_market()

    def _signal_handler(self, signum, frame):
        print("Signal received, saving state...")
        self._save_state()
        print("State saved. Exiting.")
        exit(0)

    def choose_direction(self) -> OrderDirection:
        return random.choice(self.orders_direction)

    def get_yield_value_by_direction(
        self, isin: str, direction: OrderDirection
    ) -> float:
        return self.get_value_market(isin, direction)

    def choose_isin(self) -> str:
        return random.choice(self.securities)

    def generate_key(self, isin: str, direction: OrderDirection) -> str:
        return f"{isin}_{direction.value}"

    def get_isin_and_direction_from_key(self) -> tuple[str, OrderDirection]:
        isin = self.choose_isin()
        direction = self.choose_direction()
        key = self.generate_key(isin, direction)
        if self.last_security == key:
            print("Skipping same security as last iteration.")
            # Avoid repeating the same security and direction
            isin = self.choose_isin()
            direction = self.choose_direction()
            key = self.generate_key(isin, direction)
            self.last_security = key
            return isin, direction
        return isin, direction

    def make_match(
        self, new_yield: float, isin: str, direction: OrderDirection
    ) -> bool:
        opposite_direction = self.get_opposite_direction(direction)
        opposite_yield = self.get_yield_value_by_direction(isin, opposite_direction)

        if direction == OrderDirection.BID:
            return new_yield <= opposite_yield
        return new_yield >= opposite_yield

    def generate_new_yield_by_direction(
        self, current_yield: float, direction: OrderDirection
    ) -> float:
        if direction == "bid":
            return current_yield + self.base_point
        else:
            return current_yield - self.base_point

    def get_opposite_direction(self, direction: OrderDirection) -> OrderDirection:
        return (
            OrderDirection.ASK
            if direction == OrderDirection.BID
            else OrderDirection.ASK
        )

    def set_value_market(self, isin: str, direction: OrderDirection, new_yield: float):
        self.market_dict[isin][direction.value] = new_yield

    def get_value_market(self, isin: str, direction: OrderDirection) -> float:
        return self.market_dict[isin][direction.value]

    def check_is_yield_valid(self, yield_value: float) -> bool:
        # this is our lower bound
        print(f"Checking if yield {yield_value} is valid...")
        return 8.0 < yield_value and yield_value < 15.0

    def adjust_yield_if_invalid(
        self, yield_value: float, isin: str, direction: OrderDirection
    ) -> float:
        if self.check_is_yield_valid(yield_value):
            return yield_value

        print("++++++++++++++++++++++++++++++++++")
        print(f"Yield {yield_value} is out of bounds. Adjusting...")
        ## only take the opposite direction into account
        opposite_direction = self.get_opposite_direction(direction)
        opposite_yield = self.get_yield_value_by_direction(isin, opposite_direction)
        if self.check_is_yield_valid(opposite_yield):
            if direction == "bid":
                return opposite_yield + self.default_diff + self.base_point
            else:
                return opposite_yield - self.default_diff - self.base_point
        else:
            return self.base_yield

    def bulk_order_creation(self):
        import signal

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self._load_state()

        limit_iteration = 500
        while limit_iteration > 0:
            limit_iteration -= 1
            isin, direction = self.get_isin_and_direction_from_key()

            current_yield = self.get_yield_value_by_direction(isin, direction)
            new_yield = self.generate_new_yield_by_direction(current_yield, direction)
            while self.make_match(
                new_yield, isin, direction
            ) or not self.check_is_yield_valid(new_yield):
                print(
                    f"Match detected for {isin} {direction}. Adjusting yield to avoid match."
                )
                new_yield = self.generate_new_yield_by_direction(new_yield, direction)
                new_yield = self.adjust_yield_if_invalid(new_yield, isin, direction)
                print(f"Adjusted new yield for {isin} {direction} to {new_yield}")

            print(f"Updating {isin} {direction} from {current_yield} to {new_yield}")

            self.set_value_market(isin, direction, new_yield)

            order_payload = OrdersPayloadFactory.create(
                direction=direction,
                expiration="day",
                order_type=OrderType.LIMIT,
                quantity="100",
                security_id=isin,
                yield_value=f"{new_yield:.4f}",
            )
            create_order(order_payload)

            if self.debug:
                time.sleep(0.1)
            else:
                time.sleep(0.1)


# def simulate_market_volatility():
#     print("Starting market volatility simulation...")
#     print(f"Using a time sleep of {SLEEP_TIME_POST_QUOTE_FEED} between quote feeds.")
#     simulator = MarketSimulator(
#         quote_id=QUOTE_ID, time_sleep=SLEEP_TIME_POST_QUOTE_FEED
#     )
#     simulator.bulk_order_creation()
def create_bulk_orders():
    print("Starting bulk order creation simulation...")
    print(f"Using a time sleep of {SLEEP_TIME_POST_QUOTE_FEED} between quote feeds.")
    simulator = CreateBulkOrders(
        quote_id=QUOTE_ID, time_sleep=SLEEP_TIME_POST_QUOTE_FEED
    )
    simulator.bulk_order_creation()


if __name__ == "__main__":
    create_bulk_orders()
