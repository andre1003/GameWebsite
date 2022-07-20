# Website do Scrum XPerience

Este é o repositório do site do Scrum XPerience, o qual consiste em um jogo educativo voltado para o ensino de Scrum e _eXtreme Programming_ (XP). O repositório do jogo pode ser acessado [aqui](https://github.com/andre1003/Scrum-XPerience).

## 💻 Pré-requisitos

* [Django 2.2.5](https://www.djangoproject.com/) - Framework Python para Web
* [PostgreSQL v13.4](https://www.postgresql.org/) - SGBD PostgreSQL

## ☕ Utilizando o Site do Scrum XPerience

Após clonar o repositório, é necessário realizar a configuração do PostgreSQL como SGBD. A seguir, segue os comandos para realizar a configuração do PostgreSQL via terminal Linux:

```
$ su - postgres
$ psql
=# CREATE DATABASE <nome_banco>;
=# CREATE USER <usuario> WITH PASSWORD '<senha>';
=# ALTER ROLE <usuario> SET client_encoding TO 'utf8';
=# ALTER ROLE <usuario> SET default_transaction_isolation TO 'read committed';
=# ALTER ROLE <usuario> SET timezone TO 'UTC';
=# GRANT ALL PRIVILEGES ON DATABASE <nome_banco> TO <usuario>;

# Caso seja necessário trocar a senha:
=# ALTER USER <usuario> WITH ENCRYPTED PASSWORD '<nova_senha>';
```

Após isso, é necessário realizar a configuração das váriaveis do banco de dados. Assim, acesse o arquivo ```website/settings.py``` e edite a seguinte parte:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('Nome do banco de dados', default=''), 
        'USER': config('Nome de usuário administrador', default=''), 
        'PASSWORD': config('Senha do banco de dados', default=''),
        'HOST': config('Servidor host', default='localhost'), 
        'PORT': config('Porta do banco de dados', default=5432, cast=int), # O padrão do PostgreSQL é a porta 5432
    }
}
```

Por fim, inicialize o site com o comando:

```
$ python manage.py runserver

# Caso seja necessário, execute:
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```

E pronto! Agora basta realizar as configurações de URL no Scrum XPerience, conforme descrito no repositório do executável do jogo, para poder utilizá-lo.

[⬆ Voltar ao topo](#website-do-scrum-xperience)<br>
