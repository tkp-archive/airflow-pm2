# airflow-pm2
Custom Apache Airflow operator for launching pm2 tasks

[![Build Status](https://github.com/iexcloud/airflow-pm2/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/iexcloud/airflow-pm2/actions?query=workflow%3A%22Build+Status%22)
[![Coverage](https://codecov.io/gh/iexcloud/airflow-pm2/branch/main/graph/badge.svg?token=ag2j2TV2wE)](https://codecov.io/gh/iexcloud/airflow-pm2)
[![License](https://img.shields.io/github/license/iexcloud/airflow-pm2.svg)](https://github.com/iexcloud/airflow-pm2)
[![PyPI](https://img.shields.io/pypi/v/airflow-pm2.svg)](https://pypi.python.org/pypi/airflow-pm2/)


```python
from airflow.models import DAG
from airflow_pm2 import PM2Operator

ecosystem = '''{
  "name" : "node-app-1",
  "script" : "app.js",
  "cwd" : "/srv/node-app-1/current"
}'''

dag = DAG(
    dag_id='example_pm2_operator',
    schedule_interval='0 0 * * *'
)

operator = PM2Operator(
    task_id="myjob",
    ecosystem=ecosystem,
)

if __name__ == "__main__":
    dag.cli()

```


