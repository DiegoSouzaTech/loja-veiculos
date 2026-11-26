# Recife Motors

Site de loja de veículos (catálogo digital) feito com Django.

> Projeto em desenvolvimento.

## Como rodar

1. Crie e ative um ambiente virtual (Python 3.13)
2. `pip install -r requirements.txt`
3. Copie `.env.example` para `.env` e defina a `SECRET_KEY`
4. `python manage.py migrate`
5. `python manage.py createsuperuser`
6. `python manage.py runserver`

O painel administrativo fica em `/gestao/`.
