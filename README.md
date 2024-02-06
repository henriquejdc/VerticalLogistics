### Vertical Logistics System RestAPI
**Abordagem:** 

Utilizado o Django Rest Framework para a criação de um sistema de logística de pedidos.

Criado os objetos em banco relacional **(PostgreSQL/SQLite)**:

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
- products (Product)

O total de cada pedido é calculado a partir da soma dos valores dos produtos.

Criado o app logistics e o viewset OrderViewSet (Order) onde:

- **POST /v1/orders-by-user/** que recebe o arquivo .txt criando os objetos em banco
- **GET /v1/orders-by-user/** que retorna os pedidos agrupados por usuário
    **Filtros:**

      order_id: Identificador do pedido (Int)
    
      date__gte: Data inicial (%Y-%m-%d)
    
      date__lte: Data final (%Y-%m-%d)


- **GET /v1/orders-by-user/{order_id}/** que retorna o pedido agrupado pelo usuário

**Por que desta abordagem?**

**Por que usei o Django Rest?** Utilizei está abordaggem pelo meu conhecimento em Django Rest

e por já ter um projeto base para a criação de sistemas com autenticação, base de viewset e testes.

**Por que usei o banco relacional?** Por ser um banco de dados que facilita a busca de dados e reduz a duplicidade, 

além de que é facilmente integrado ao Django e possui suporte para consultar com filtros e ordenação.

**Por que usei o Docker?** Utilizei o Docker para facilitar a execução do projeto em qualquer ambiente,


### Docker PostgreSQL:
```
You need to create .env like example_env file

sudo docker-compose -f docker-compose-postgresql.yml up
```


### Docker SQLite3:
```
sudo docker-compose -f docker-compose-sqlite.yml up
```


### Configurations .env: 
```
Copy .env.example to .env
Set your environment variables on .env file
Use variables with the same names as you use when creating the database
```


### Environment: 
Python Version 3.8.10
```
python3 -m venv venv 
OR
virtualenv --python=python3 venv

source venv/bin/activate

cd django/
```


### Database - POSTGRES (Linux): 
```
sudo -i -u postgres
psql
CREATE USER user_default WITH PASSWORD 'password_default';
ALTER USER user_default CREATEDB;
CREATE DATABASE vl_database;
ALTER DATABASE vl_database OWNER TO user_default;
CREATE EXTENSION pg_trgm;
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


### Create User and Access Token in API: 
```
Use endpoint /auth/signup/ 
Before use /auth/jwt/create/ 

Now you have your access_token and refresh_token
```


### Use Authenticate Token: 
```
Bearer {access_token}
```


### Create Super User / Login: 
```
python manage.py createsuperuser 

To login use email and password

Already have a super user in database: admin@admin.com / admin
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
HTML report: django/htmlcov/index.html
```


### New translations:
```
python manage.py makemessages --locale pt_BR

Change to pt-br on settings:
LANGUAGE_CODE= 'pt-BT'

Obs: If necessary translate to portuguese.
```

## Copyright and license

Code released under the [freeBSD License](https://github.com/Henriquejdc/VerticalLogistics/blob/master/LICENSE.md).
