#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


"""
### ETL DAG Tutorial Documentation
This ETL DAG is compatible with Airflow 1.10.x (specifically tested with 1.10.12) and is referenced
as part of the documentation that goes along with the Airflow Functional DAG tutorial located
[here](https://airflow.apache.org/tutorial_decorated_flows.html)
"""
# [START tutorial]
# [START import_module]
import json
from datetime import datetime
from textwrap import dedent


# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator

# [END import_module]

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
}
# [END default_args]

# [START instantiate_dag]
with DAG(
    'tournament_scores_etl',
    default_args=default_args,
    description='Tournament Scores ETL',
    #schedule_interval='*/5 * * * * *',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['scores'],
) as dag:
    # [END instantiate_dag]
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]

    # [START extract_function]
    def extract(**kwargs):
        ti = kwargs['ti']
        #data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        #ti.xcom_push('order_data', data_string)

        import numpy as np
        import pandas as pd
        import requests 

        url = "https://live-golf-data.p.rapidapi.com/leaderboard"

        querystring = {"tournId":"004","year":"2022"}

        headers = {
        'x-rapidapi-host': "live-golf-data.p.rapidapi.com",
        'x-rapidapi-key': "61ac0c86e6msh348d8e602f15c14p1d225bjsn6c2420358e9e"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        output = response.json()

        with open('json_data.json', 'w') as outfile:
            json.dump(output, outfile)

        headerData = pd.json_normalize(data=output)
        leaderData = pd.json_normalize(data=output['leaderboardRows'], record_path=['rounds'], meta=['lastName', 'firstName','playerId', 'status', 'total', 'currentRoundScore', 'position'])

        headerData.to_csv('headerData.csv')
        leaderData.to_csv('leaderData.csv')


    # [END extract_function]

    # [START transform_function]
    def transform(**kwargs):
        ti = kwargs['ti']
        #extract_data_string = ti.xcom_pull(task_ids='extract', key='order_data')
        #order_data = json.loads(extract_data_string)

        #total_order_value = 0
        #for value in order_data.values():
        #    total_order_value += value

        #total_value = {"total_order_value": total_order_value}
        #total_value_json_string = json.dumps(total_value)
        #ti.xcom_push('total_order_value', total_value_json_string)

        import numpy as np
        import pandas as pd
        from pyspark.sql import SparkSession
        from pyspark import SparkContext
        from pyspark.conf import SparkConf

        conf = SparkConf()
        conf.setAll(
        [
            ('spark.app.name', 'pysparktest'),
            ('spark.master', 'spark://spark-master:7077'),
            ('spark.executor.memory', "512m")
        ]
        )

        spark = SparkSession.builder.config(conf=conf).getOrCreate()
        """
        headerData = pd.read_csv('headerData.csv')
        leaderData = pd.read_csv('leaderData.csv')
        leaderData['tournId'] = headerData.loc[0,'tournId']
        leaderData['year'] = headerData.loc[0,'year']
        leaderData['tournStatus'] = headerData.loc[0,'status']
        leaderData['currentRound'] = headerData.loc[0,'roundId.$numberInt']
        leaderData['currentRoundStatus'] = headerData.loc[0,'roundStatus']
        leaderData['roundId'] = leaderData['roundId.$numberInt']
        leaderData['strokes'] = leaderData['strokes.$numberInt']

        leaderData=leaderData[['tournId','year','tournStatus','currentRound','currentRoundStatus','playerId','lastName','firstName','position','total','roundId','scoreToPar','strokes']]
        leaderData = leaderData[leaderData['roundId']== 4]

        leaderData.to_csv("golf.csv")
        """
        spark.stop()

    # [END transform_function]

    # [START load_function]
    def load(**kwargs):
        ti = kwargs['ti']
        total_value_string = ti.xcom_pull(task_ids='transform', key='total_order_value')
        total_order_value = json.loads(total_value_string)

        print(total_order_value)

    # [END load_function]

    # [START main_flow]
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )
    extract_task.doc_md = dedent(
        """\
    #### Extract task
    A simple Extract task to get data ready for the rest of the data pipeline.
    In this case, getting data is simulated by reading from a hardcoded JSON string.
    This data is then put into xcom, so that it can be processed by the next task.
    """
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )
    transform_task.doc_md = dedent(
        """\
    #### Transform task
    A simple Transform task which takes in the collection of order data from xcom
    and computes the total order value.
    This computed value is then put into xcom, so that it can be processed by the next task.
    """
    )

    extract_task >> transform_task #>> load_task

# [END main_flow]

# [END tutorial]