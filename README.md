# PoliStat
Website for MBHS's Political Statistics 2018 House Model

## Getting Started
**Prequisites:** Python 3+, `pipenv`, and `sass` (for static precompilation)

### Quick Start
 1. Clone this repo: `https://github.com/polistat/PoliStat.git`.
 2. Change directory to `polistat`: `cd polistat`.
 3. Create new virtual environment: `pipenv install --dev`.
 4. Run `pipenv shell` to enter the new environment.
 5. Make migrations and apply:
    - `python manage.py makemigrations figures`
    - `python manage.py migrate`
 6. Load testing data:
    - `python manage.py loaddata fixtures/states`
    - `python manage.py loaddata fixtures/districts`
 7. Run server: `python manage.py runserver`.
 8. Visit in browser: `localhost:8000`.
 9. And voila!

### Admin Page
Django comes shipped with an authentication app, which we use for all our admin
needs. Just run `python manage.py createsuperuser`, follow the instructions, run the server,
and visit `localhost:8000/admin` to log in.

#### Contributions
We welcome any outside contributions! Just make a fork and submit a pull request.
