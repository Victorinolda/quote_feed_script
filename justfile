
init:
    -cp --no-clobber .env.example .env
    pipenv install --dev

simulate:
    pipenv run python3 main.py multiple 10

single:
    pipenv run python3 main.py single 10

both:
    pipenv run python3 main.py single 10 both
