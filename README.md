### Logistics System RestAPI
**Abordagem:** 

Utilizado o Django Rest Framework para a criação de um sistema de logística de pedidos.

Criado os objetos em banco **postgreSQL**:

**UserVL** 
- user_id
- name

**Product** 
- product_id
- value

**Order** 
- order_id
- date
- user (UserVL)
- product (Product)

O total de cada pedido é calculado a partir da soma dos valores dos produtos.

Criado o app logistics e o viewset OrderViewSet (Order) onde:

- POST /v1/orders-by-user/ que recebe o arquivo .txt criando os objetos em banco
- GET /v1/orders-by-user/ que retorna os pedidos agrupados por usuário
- GET /v1/orders-by-user/{order_id}/ que retorna os pedido agrupado pelo usuário

**Por que desta abordagem?**

**Por que usei o Django Rest?** Utilizei está abordaggem pelo meu conhecimento em Django Rest

e por já ter um projeto base para a criação de sistemas com autenticação, base de viewset e testes.

**Por que usei o postgreSQL?** Por ser um banco de dados robusto e que suporta grande quantidade de dados, 

além de que é facilmente integrado ao Django e possui suporte para consultar com filtros e ordenação.


### Environment: 
Python Version 3.8.10
```
python3 -m venv venv 
OR
virtualenv --python=python3 venv

source venv/bin/activate

cd src/django/
```


### Database - POSTGRES (Linux): 
```
sudo -i -u postgres
psql
CREATE USER user_default WITH PASSWORD 'defaultdatabase';
ALTER USER user_default CREATEDB;
CREATE DATABASE default_database;
ALTER DATABASE default_database OWNER TO user_default;
CREATE EXTENSION pg_trgm;
```


### Configurations .env: 
```
Copy .env.example to .env
Set your environment variables on .env file
Use variables with the same names as you use when creating the database
```


### Requirements: 
```
pip install -r requirements.txt
```


### Migration: 
```
python manage.py migrate
```


### Collect Staticfiles: 
```
python manage.py collectstatic   
```


### Run: 
```
python manage.py runserver
```


### Documentation: 
```
/docs
/docs/redoc
```


### Create Super User / Login: 
```
python manage.py createsuperuser 

To login use email and password
```


### Unit Tests: 
```
python manage.py test --failfast logistics
```

### Unit Tests Report HTML: 
```
coverage run --source='./logistics' manage.py test
coverage report

coverage html
```


### New translations:
```
python manage.py makemessages --locale pt_BR

Change to pt-br on settings:
LANGUAGE_CODE= 'pt-BT'

Obs: Necessary translate to portuguese.
```


### Create User and Access Token: 
```
Use endpoint /auth/signup/ 
Before use /auth/jwt/create/ 

Now you have your access_token and refresh_token
```


### Use Authenticate Token: 
```
Bearer {access_token}
```

