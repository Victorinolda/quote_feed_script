init:
    -cp --no-clobber .env.example .env.local
    pipenv install --dev

# Run with multiple streams execution (local env, yield 10)
multiple env="local":
    pipenv run python3 main.py --env {{env}} --execution multiple --yield 10

# Run with single stream execution (local env, yield 10)
single env="local":
    pipenv run python3 main.py --env {{env}} --execution single --yield 10

# Run with both directions (local env, yield 9.99, direction both)
both env="local":
    pipenv run python3 main.py --env {{env}} --execution single --yield 9.99 --direction both

# Run market simulation (local env)
simulate env="local":
    pipenv run python3 main.py --env {{env}} --execution simulate
