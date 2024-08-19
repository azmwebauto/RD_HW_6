### 1. Installation
~~~bash
poetry install
~~~

### 2. Environment configuration
create .env file in root directory using example.env

### 3. Run migrations
~~~bash
alembic upgrade heads
~~~

### 4. Download CVEs using git clone
~~~bash
git clone https://github.com/CVEProject/cvelistV5 --depth=1
~~~

### 4. Run python script to insert data into Postgres
~~~bash
poetry run python main.py -f ./cvelistV5/cves
~~~
