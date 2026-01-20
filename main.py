import os
from pathlib import Path
from dotenv import load_dotenv

BASE_YIELD = 10  # Default yield value
DEFAULT_DIRECTION = "bid"  # Default direction for yield values
DEFAULT_EXECUTION = "single"  # Default execution type
DEFAULT_ENV = "local"  # Default environment


def load_env_file(env: str):
    """Load the appropriate .env file based on the environment."""
    env_lower = env.lower()
    env_file = Path(f".env.{env_lower}")
    
    if env_file.exists():
        print(f"Loading environment from: {env_file}")
        load_dotenv(env_file)
    else:
        print(f"Warning: .env.{env_lower} not found, falling back to .env")
        # Try to load default .env file
        if Path(".env").exists():
            load_dotenv(".env")
        else:
            print("No .env files found")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Process quote feeds with configurable execution types and parameters"
    )
    parser.add_argument(
        "--env",
        "-e",
        type=str,
        default=DEFAULT_ENV,
        help=f"Environment to load (.env.<env>) - default: {DEFAULT_ENV}",
    )
    parser.add_argument(
        "--execution",
        type=str,
        default=DEFAULT_EXECUTION,
        choices=["single", "multiple", "simulate"],
        help=f"Execution type - default: {DEFAULT_EXECUTION}",
    )
    parser.add_argument(
        "--yield",
        type=float,
        default=BASE_YIELD,
        dest="yield_value",
        help=f"Base yield value - default: {BASE_YIELD}",
    )
    parser.add_argument(
        "--direction",
        "-d",
        type=str,
        default=DEFAULT_DIRECTION,
        choices=["bid", "ask", "both"],
        help=f"Direction for yield values - default: {DEFAULT_DIRECTION}",
    )

    parsed_args = parser.parse_args()

    environment = parsed_args.env
    load_env_file(environment)

    execution_type = parsed_args.execution
    yield_as_float = parsed_args.yield_value
    direction = parsed_args.direction

    print(f"Environment: {environment}")
    print(f"using yield {yield_as_float}")

    if execution_type == "single":
        from single_stream import process_single_stream

        process_single_stream(yield_as_float, direction=direction)
    elif execution_type == "multiple":
        from multiple_streams import process_multiple_streams

        process_multiple_streams(yield_value=yield_as_float)
    elif execution_type == "simulate":
        from simulate_market import simulate_market_volatility

        simulate_market_volatility()


if __name__ == "__main__":
    main()
