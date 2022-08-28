# traffic_accidents_ETL_airflow
Extracción, procesamiento y visualización de colisiones dobles en Madrid, España

## Requirements

* docker
* folium
* googlemaps
* pandas
* psycopg2 
* airflow

## Installation

```bash
python -m pip install -r requirements.txt
```

# Execution as python modules
Run data transform
```bash
python -m traffic_accidents
```
Generate traffic accidents' map
```bash
python -m mc_map_generator std_map
```
Generate traffic accidents' heatmap
```bash
python -m mc_map_generator heatmap
```

# Execution using apache-airflow

## Start a postgres instance

Start a postgres instance using docker
```bash
docker run --name postgres_db2 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=airflow -p 5432:5432 -d postgres
```

## Start the web server and scheduler
```bash
airflow webserver -p 8080
airflow scheduler
```
and then open `http://localhost:8080`
