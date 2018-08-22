#!/usr/bin/env python
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime

from desktop.lib.django_util import render

from kafka.kafka_client import KafkaApi
from kafka.kafka_api import get_topics
from metadata.manager_client import ManagerApi


def index(request):
  kafka_api = KafkaApi()
  manager_api = ManagerApi()

  return render('index.mako', request, {
    'has_kafka_service': manager_api.has_service('KAFKA'),
    'has_kafka_topic': 'traffic' in get_topics(),
    'has_kudu_service': manager_api.has_service('KUDU'),
    'is_embeddable': request.GET.get('is_embeddable', False),
  })


def data(request):
  return render('data.mako', request, {
  })


def check_has_kafka():
  pass

def check_has_kafka_topic():
  pass

def check_has_kudu():
  pass

def check_has_kudu_table():
  pass

def create_table():
  pass


create_table_query = '''
CREATE DATABASE IF NOT EXISTS traffic;
DROP TABLE IF EXISTS traffic.conditions;

CREATE TABLE traffic.conditions
(
    as_of_time BIGINT
  , avg_num_veh DOUBLE
  , min_num_veh INT
  , max_num_veh INT
  , first_meas_time BIGINT
  , last_meas_time BIGINT
  , PRIMARY KEY(as_of_time)
)
PARTITION BY HASH PARTITIONS 4
STORED AS KUDU
;
'''