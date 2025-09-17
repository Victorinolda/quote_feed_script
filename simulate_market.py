import random
from typing import Dict, Mapping
import time
from lib.quoute_feed import QuoteFeed, QuoteFeedFactory, post_quote_feed_without_sleep
import json

from config.config import QUOTE_ID,SLEEP_TIME_POST_QUOTE_FEED
from lib.securities import get_active_securities_isin 


class MarketSimulator:
    securities: list[str] = []
    quote_id: str
    market_dict: Dict[str, Dict[str, float]] = {}
    last_security: str | None
    base_yield: float = 11.0
    orders_direction:list[str] = ["bid", "ask"]
    base_point:float = 0.01
    _file_path: str
    default_diff:float = 0.1
    debug: bool = False
    time_sleep: int


    def __init__(self, quote_id: str,time_sleep:int,debug: bool = False):
        self.quote_id = quote_id
        self.time_sleep = time_sleep
        self.last_security = None
        self._file_path = "market_simulator_state.json"
        self.debug = debug

    def generate_initial_market_dict(self):
        market_dict: Dict[str, Dict[str, float]] = dict()
        for isin in self.securities:
            yield_ask_value = self.base_yield - self.base_point - self.default_diff
            yield_bid_value = self.base_yield + self.base_point
            market_dict[isin] = {
                "ask": yield_ask_value,
                "bid": yield_bid_value
            }
        self.market_dict = market_dict

    def get_securities(self):
        # Example securities list; replace with actual securities retrieval logic
        if self.debug:
            self.securities = [ "ISIN01"]
            return
        self.securities = get_active_securities_isin()

    def initialize_market(self):
        self.get_securities()
        if not self.securities:
            print("No active securities found.")
            return
        self.generate_initial_market_dict()

    def _save_state(self):
        with open(self._file_path, 'w') as f:
            json.dump(self.market_dict, f)

    def _load_state(self):
        try:
            with open(self._file_path, 'r') as f:
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

    def choose_direction(self) -> str:
        return random.choice(self.orders_direction)

    def get_yield_value_by_direction(self,isin:str, direction:str) -> float:
        return self.market_dict[isin][direction]

    def choose_isin(self) -> str:
        return random.choice(self.securities)

    def generate_key(self, isin: str, direction: str) -> str:
        return f"{isin}_{direction}"

    def get_isin_and_direction_from_key(self) -> tuple[str, str]:
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

    def make_match(self, new_yield:float,isin:str, direction:str) -> bool:
        opposite_direction = self.get_opposite_direction(direction)
        opposite_yield = self.get_yield_value_by_direction(isin,opposite_direction)

        if direction == "bid":
            return new_yield <= opposite_yield
        return new_yield >= opposite_yield


    def generate_new_yield_by_direction(self, current_yield:float, direction:str) -> float:
        if direction == "bid":
            return current_yield + self.base_point
        else:
            return current_yield - self.base_point

    def get_opposite_direction(self, direction:str) -> str:
        return "ask" if direction == "bid" else "bid"

    def _create_payload(self, isin:str, direction:str, new_yield:float) -> QuoteFeed:
        return QuoteFeedFactory.create(
            isin=isin,
            data_type=direction,
            value=new_yield,
            quote_feed_id=self.quote_id
        )
    def post_payload(self, payload:QuoteFeed):
        if self.debug:
            print(f"Posting payload: {payload}")
            return
        post_quote_feed_without_sleep(payload)

    def check_is_yield_valid(self, yield_value:float) -> bool:
        #this is our lower bound
        print(f"Checking if yield {yield_value} is valid...")
        return  8.0 < yield_value and yield_value < 15.0

    def adjust_yield_if_invalid(self, yield_value:float,isin:str, direction:str) -> float:
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




    def simulate_volatility(self):
        import signal
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self._load_state()

        while True:
            isin, direction = self.get_isin_and_direction_from_key()

            current_yield = self.get_yield_value_by_direction(isin, direction)
            new_yield = self.generate_new_yield_by_direction(
                current_yield, 
                direction
            )
            # if self.debug:
            #     inverse_direction = self.get_opposite_direction(direction)
            #     inverse_yield = self.get_yield_value_by_direction(isin, inverse_direction)
            #     print("***")
            #     print(f"Current yield for {isin} {direction}: {current_yield}")
            #     print(f"Proposed new yield for {isin} {direction}: {new_yield}")
            #     print(f"Current yield for {isin} {inverse_direction}: {inverse_yield}")
            #     print("make_match:", self.make_match(new_yield, isin, direction))

            while self.make_match(new_yield, isin, direction) or not self.check_is_yield_valid(new_yield):
                print(f"Match detected for {isin} {direction}. Adjusting yield to avoid match.")
                new_yield = self.generate_new_yield_by_direction(new_yield, direction)
                new_yield = self.adjust_yield_if_invalid(new_yield, isin, direction)
                print(f"Adjusted new yield for {isin} {direction} to {new_yield}")

            print(f"Updating {isin} {direction} from {current_yield} to {new_yield}")

            self.market_dict[isin][direction] = new_yield

            payload = self._create_payload(isin, direction, new_yield)
            self.post_payload(payload)

            if self.debug:
                time.sleep(0.1)
            else:
                time.sleep(self.time_sleep)


def simulate_market_volatility():
    simulator = MarketSimulator(quote_id=QUOTE_ID, time_sleep=SLEEP_TIME_POST_QUOTE_FEED)
    simulator.simulate_volatility()
