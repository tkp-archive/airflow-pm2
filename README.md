# airflow-pm2
Custom Apache Airflow operator for launching pm2 tasks


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


