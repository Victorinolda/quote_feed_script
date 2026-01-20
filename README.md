# quote_feed_script

to run this script, you need to run the following commands:

```bash
direnv allow
```

after that, to start the script, run:

```bash
just init
```

this will copy the `.env.example` file to `.env.local` and install the dependencies using pipenv.
by default the `.env.local`file is created, but you can create any other file like `.env.dev` or `.env.qa`,
to use a diferent environment, you can run any of the following commands with the correct environment name:

By default every command uses the `.env.local` file, but you can specify another env file by adding the env name after the command.

```bash
just multiple env
```

this will run the script to create quotes for every m-bono active in the specified environment.

```bash
just single direction env
```

this will create qoutes for the specified security find in the env file, for a single direction (ask or bid).
by default it will create for the ask direction in the local environment.

```bash
just both env
```

this will create qoutes for the specified security find in the env file, for ask and bid directions.

```bash
just simulate env
```

this will simulate a market volatility for all the actives securities with a sleep time, that can we modifiend in the env file
for the specified environment.
