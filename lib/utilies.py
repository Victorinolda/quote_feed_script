
import time

from config.config import NUMBER_OF_QUOTES
def countdown(n:int):
    if n == 0:
        return
    time.sleep(1)
    print("*************")
    print(f"seconds {n}")
    countdown(n - 1)

def generate_array_yield(base_yield:float, n:int=NUMBER_OF_QUOTES, direction="bid"):
    #this generate a array of yields that have a difference of 0.01,
    # for example [ 7.123, 7.113, 7.103, ..... ]
    # NOTE: if you need ask change the minus (-) sign for the plus sign
    if direction == "ask":
        yiel_value = (base_yield - 0.01 * (len(range(n)) + 1))
        return [yiel_value - i * 0.001 for i in range(n)]
    return [(base_yield) + i * 0.001 for i in range(n)]


def new_time_stamp() -> str:
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    iso_timestamp = now.isoformat(timespec='milliseconds').replace('+00:00', 'Z')

    return iso_timestamp
