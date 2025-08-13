# quote_feed_script

to run this script, you need to run the following commands:

```bash
direnv allow
```

after that, to start the script, run:

```bash
just init
```

this will copy the `.env.example` file to `.env` and install the dependencies.

before running the script, you need to set the environment variables in the `.env` file. You can use the `.env.example` file as a reference.
after setting the environment variables, you can run some of the following commands:

```bash
just simulate
```

- this will run the script to create multiple quotes for all the active securities, with a yield of 10

```bash
just single
```

- this will create a single quote for the security specified in the `.env` file, with a yield of 10

```bash
just both
```

- this will create ask and bid quotes for the security specified in the `.env` file, with a yield of 10

if you need to run the script with a different yield, you can run the following command:

```bash
pipenv run python main.py multiple <yield>
```

this will run the script to create multiple quotes for all the active securities, with the specified yield.
or

```bash
pipenv run python main.py single <direction>  <yield>
```

this will create a single quote for the security specified in the `.env` file, with the specified yield and direction (ask, bid or both).
