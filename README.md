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
`--file - полный путь к файлу`
`--max_open_file_limit - максимальное колличество файлов для чтения, по дефолту 1000`
~~~bash
poetry run python main.py -f ./cvelistV5/cves --max_open_file_limit 1000
~~~
