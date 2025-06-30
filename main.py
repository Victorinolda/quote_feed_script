BASE_YIELD = 10 # Default yield value
DEFAULT_DIRECTION = "bid"  # Default direction for yield values
DEFAULT_EXECUTION = "single"  # Default execution type

def main():
    import sys
    args = sys.argv[1:]

    yield_as_float = BASE_YIELD
    direction = DEFAULT_DIRECTION
    execution_type = DEFAULT_EXECUTION

    if len(args) > 0:

        execution_type = args[0] if len(args) > 0 else DEFAULT_EXECUTION
        if execution_type not in ["single", "multiple"]:
            print(f"Invalid execution type '{execution_type}', using default '{DEFAULT_EXECUTION}'")
            execution_type = DEFAULT_EXECUTION

        base_yield = args[1] if len(args) > 1 else BASE_YIELD
        print("using yield {}".format(base_yield))
        try:
            yield_as_float = float(base_yield)
        except ValueError:
            print(f"Invalid yield value '{base_yield}', using default {BASE_YIELD}")
            yield_as_float = BASE_YIELD

        base_direction = args[2] if len(args) > 2 else DEFAULT_DIRECTION
        if base_direction in ["bid", "ask", "both"]:
            direction = base_direction
        else:
            print(f"Invalid direction '{base_direction}', using default '{DEFAULT_DIRECTION}'")


    if execution_type == "single":
        from single_stream import process_single_stream
        process_single_stream(yield_as_float, direction=direction)
    elif execution_type == "multiple":
        from multiple_streams import process_multiple_streams
        process_multiple_streams(yield_value=yield_as_float)

if __name__ == "__main__":
    main()
