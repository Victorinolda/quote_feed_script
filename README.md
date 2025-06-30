# quote_feed_script

To run this script you need to have installed Pipenv and have the .env file in the root directory.

# Install dependencies

```bash
pipenv install
```

# Run into the virtual environment

```bash
pipenv shell
```

# run the script

There is two modes to run the script:

- Single mode: run the script with a single quote
- Multiple mode: run the script with multiple securities (in this moment only for m-bonos)

## Single mode

```bash
python3 main.py single yield_value direction
```

where `yield_value` is the yield value of the quote and `direction` is the direction of the quote (ask, bid and both).
by default the direction is bid and the yield value is 10
You can also config the security in the .env file with the variable `ISIN`.
Both direction send quotes for the same security in ask and bid.

## Multiple mode

```bash
python3 main.py multiple yield_value
```

where `yield_value` is the yield value of the quote, the default value is 10.
this script only work for m-bonos

# Example

```bash
python3 main.py single 10 bid
```

```bash
python3 main.py multiple 10
```
