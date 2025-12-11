
init:
    -cp --no-clobber .env.example .env
    pipenv install --dev

multiple:
    pipenv run python3 main.py multiple 10

single:
    pipenv run python3 main.py single 10

both:
    pipenv run python3 main.py single 9.99 both

simulate:
    pipenv run python3 main.py simulate
