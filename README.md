### Logistics System RestAPI
**Abordagem:** 

[//]: # (Utilizado um projeto meu de base acrescentando a)

[//]: # (o app e o viewset Coupon &#40;Cupom&#41; onde o POST /vl/)

[//]: # (trata-se da criação do cupom e o POST )

[//]: # (/vl/use_vl/ trata-se da utilização do cupom.)

**Por que desta abordagem?**

[//]: # (Acredito que um cupom não seja apenas um ID inteiro,)

[//]: # (caso fosse poderia tratar-se com o próprio POST de criação)

[//]: # (e o PUT para sua utilização/atualização.)

[//]: # ()
[//]: # (Entretanto, acredito que um cupom possa ser várias letras)

[//]: # (e números, podendo em caso de ser utilizado como chave primária)

[//]: # (prejudicar consultas e performance.)

[//]: # (Também, deixaria exposto o cupom como chave ao ser utilizado)

[//]: # (no navegador.)


### Environment: 
Python Version 3.8.10
```
python3 -m venv venv 
OR
virtualenv --python=python3 venv

source venv/bin/activate
```


### Requirements: 
```
pip install -r requirements.txt
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


### Create Super User / Login: 
```
python manage.py createsuperuser 

To login use email and password
```


### Docs: 
```
/docs
/docs/redoc
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

