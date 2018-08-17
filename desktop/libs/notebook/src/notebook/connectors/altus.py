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

import logging

from datetime import datetime,  timedelta

from django.urls import reverse
from django.utils.translation import ugettext as _

from metadata.conf import ALTUS
from navoptapi.api_lib import ApiLib


from desktop.lib.exceptions_renderable import PopupException


LOG = logging.getLogger(__name__)

DATE_FORMAT = "%Y-%m-%d"


def _exec(service, command, parameters=None):
  if parameters is None:
    parameters = {}

  if service == 'analyticdb':
    hostname = ALTUS.HOSTNAME_ANALYTICDB.get()
  elif service == 'dataeng':
    hostname = ALTUS.HOSTNAME_DATAENG.get()
  elif service == 'wa':
    hostname = ALTUS.HOSTNAME_WA.get()
  else:
    hostname = ALTUS.HOSTNAME.get()

  try:
    api = ApiLib(service, hostname, ALTUS.AUTH_KEY_ID.get(), ALTUS.AUTH_KEY_SECRET.get().replace('\\n', '\n'))
    LOG.debug('%s : %s' % (command, parameters))
    resp = api.call_api(command, parameters)
    LOG.info(resp)
    json_resp = resp.json()
    LOG.debug(json_resp)
    return json_resp
  except Exception, e:
    raise PopupException(e, title=_('Error accessing'))


class IAMApi(): pass
# altus iam list-user-assigned-roles --user=crn:altus:ia


class SdxApi():

  def __init__(self, user): pass

  def list_namespaces(self):
    """
    e.g. returns
    [{
      u'status': u'CREATED',
      u'namespaceName': u'cca-5150-ns',
      u'creationDate': u'2018-06-03T23:24:46.125000+00:00',
      u'crn': u'crn:altus:sdx:us-west-1:12a0079b-1591-4ca0-b721-a446bda74e67:namespace:cca-5150-ns/f54461af-b241-4f1d-a521-ab3624e841c4'},
      ...
    ]
    """
    data = _exec('sdx', 'listNamespaces', parameters={'maxItems': 500})
    namespaces = data['namespaces']

    while data.get('nextToken'):
      data = _exec('sdx', 'listNamespaces', parameters={'startingToken': data['nextToken']})
      namespaces.extend(data['namespaces'])

    return namespaces


class DataEngApi():

  def __init__(self, user): pass

  def list_jobs(self, submitter_crns=None, page_size=None, starting_token=None, job_statuses=None, job_ids=None, job_types=None, creation_date_before=None,
        creation_date_after=None, cluster_crn=None, order=None):
    args = {}

    if creation_date_after is None:
      creation_date_after = (datetime.today() - timedelta(days=7)).strftime(DATE_FORMAT)

    if submitter_crns:
      args['submitterCrns'] = submitter_crns
    if page_size is not None:
      args['pageSize'] = str(page_size)
    if starting_token:
      args['startingToken'] = starting_token
    if job_statuses:
      args['jobStatuses'] = job_statuses
    if job_ids:
      args['jobIds'] = job_ids
    if job_types:
      args['jobTypes'] = job_types
    if creation_date_before:
      args['creationDateBefore'] = creation_date_before
    if creation_date_after:
      args['creationDateAfter'] = creation_date_after
    if cluster_crn:
      args['clusterCrn'] = cluster_crn
    if order:
      args['order'] = order

    return _exec('dataeng', 'listJobs', args)

  def describe_job(self, job_id):
    return _exec('dataeng', 'describeJob', {'jobId': job_id})

  def submit_hive_job(self, cluster_name, script, params=None, job_xml=None):
    job = {'script': script}

    if params:
      job['params'] =  params
    if job_xml:
      job['jobXml'] =  job_xml

    return self.submit_jobs(cluster_name, [{'hiveJob': job}])

  def submit_spark_job(self, cluster_name, jars=None, main_class=None, arguments=None, spark_arguments=None, properties_file=None):
    job = {
      "jars": jars if jars else [],
      "applicationArguments": arguments if arguments else [],
      #"propertiesFile": "string"
    }
    if spark_arguments:
      job['sparkArguments'] = ' '.join(spark_arguments)
    if main_class:
      job["mainClass"] = main_class

    return self.submit_jobs(cluster_name, [{'sparkJob': job, 'name': None, 'failureAction': 'NONE'}])

  def submit_yarn_job(self):
    return _exec('dataeng', 'submitJobs')

  def submit_jobs(self, cluster_name, jobs):
    return _exec('dataeng', 'submitJobs', {'clusterName': cluster_name, 'jobs': jobs})

  def terminate_job(self, job_id):
    return _exec('dataeng', 'terminateJob', {'jobId': job_id})

  def list_clusters(self, names=None, page_size=None, starting_token=None):
    args = {}

    if names:
      args['clusterNames'] = names
    if page_size is not None:
      args['pageSize'] = str(page_size)
    if starting_token:
      args['startingToken'] = starting_token

    return _exec('dataeng', 'listClusters', args)

  def create_cluster(self, cloud_provider, cluster_name, cdh_version, public_key, instance_type, environment_name, workers_group_size=3, namespace_name=None):
    # [--cloudera-manager-username <value>]
    # [--cloudera-manager-password <value>]

    params = { # cloud_provider: AWS, Azure...
      'clusterName': cluster_name,
      'cdhVersion': cdh_version,
      'publicKey': public_key,
      'instanceType': instance_type,
      'environmentName': environment_name,
      'workersGroupSize': workers_group_size,
      #'automaticTerminationCondition': "EMPTY_JOB_QUEUE"
    }

    if namespace_name:
      params['namespaceName'] = namespace_name

    params = {
      u'additionalClusterResourceTags': [],
      u'automaticTerminationCondition': u'NONE',
      u'cdhVersion': u'CDH514',
      u'clouderaManagerPassword': u'guest',
      u'clouderaManagerUsername': u'guest',
      u'clusterName': u'analytics4',
      u'computeWorkersConfiguration': {
        u'bidUSDPerHr': 0,
        u'groupSize': 0,
        u'useSpot': False
      },
      u'environmentName': u'crn:altus:environments:us-west-1:12a0079b-1591-4ca0-b721-a446bda74e67:environment:analytics/236ebdda-18bd-428a-9d2b-cd6973d42946',
      u'instanceBootstrapScript': u'',
      u'instanceType': u'm4.xlarge',
      u'jobSubmissionGroupName': u'',
      u'jobs': [{
        u'failureAction': u'INTERRUPT_JOB_QUEUE',
        u'name': u'a87e20d7-5c0d-49ee-ab37-625fa2803d51',
        u'sparkJob': {
          u'applicationArguments': [u'filesystems3.conf'],
          u'jars': [u's3a://datawarehouse-customer360/ETL/envelope-0.6.0-SNAPSHOT-c6.jar'],
          u'mainClass': u'com.cloudera.labs.envelope.EnvelopeMain',
          u'sparkArguments': u'--archives=s3a://datawarehouse-customer360/ETL/filesystems3.conf'}
        }
      ],
      u'namespaceName': u'crn:altus:sdx:us-west-1:12a0079b-1591-4ca0-b721-a446bda74e67:namespace:analytics/7ea35fe5-dbc9-4b17-92b1-97a1ab32e410',
      u'publicKey': u'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDuTEfNIW8LEcVgprUrourbYjoW1RaTLhfzPnnBjJrg14koQrosl+s9phrpBBLTWmQuQdvy9iC2ma//gY5nz/7e+QuaeENhhoEiZn1PDBbFakD/AOjZXIu6DTEgCrOeXsQauFZKOkcFvrBGJC0qigYU3b8Eys4cun3RQ4S9WkDW6538wOSnsm6sXcL84KqbH+ay5gTk+lz3bi/6plALZMItbRz9IulXnLM4QfCwMxXTU/IjtnT+ltZVvKsWpfvDQ3Oyu/a6gK369iXcSP0e07KAzWiv2WYX46sNzZ8+de9ho1/VMaXnI4WrooV9lxByKWD+WsXkqtctT16VfxpX8CeR romain@unreal\n',
      u'serviceType': u'SPARK',
      u'workersConfiguration': {},
      u'workersGroupSize': u'3'
  }

    return _exec('dataeng', 'createAWSCluster', params)

  def delete_cluster(self, cluster_id):
    return _exec('dataeng', 'deleteCluster', {'clusterName': cluster_id})

  def describe_clusters(self):
    return _exec('dataeng', 'describeCluster')


class AnalyticDbApi():

  def __init__(self, user): pass

  def create_cluster(self, cloud_provider, cluster_name, cdh_version, public_key, instance_type, environment_name, workers_group_size=3, namespace_name=None):
    # [--cloudera-manager-username <value>]
    # [--cloudera-manager-password <value>]

    params = { # cloud_provider: AWS, Azure...
      'clusterName': cluster_name,
      'cdhVersion': cdh_version,
      'publicKey': public_key,
      'instanceType': instance_type,
      'environmentName': environment_name,
      'workersGroupSize': workers_group_size
    }

    if namespace_name:
      params['namespaceName'] = namespace_name

    return _exec('analyticdb', 'createAWSCluster', params)

  def list_clusters(self):
    """
    e.g. returns
    [{
            "status": "CREATED",
            "namespaceCrn": "crn:altus:sdx:us-west-1:12a0079b-1591-4ca0-b721-a446bda74e67:namespace:spot-ns/7bdb225f-a7a1-408e-8503-1b3a422cc039",
            "workersGroupSize": 4,
            "clusterName": "spot",
            "environmentType": "AWS",
            "secured": false,
            "environmentCrn": "crn:altus:environments:us-west-1:12a0079b-1591-4ca0-b721-a446bda74e67:environment:Spot-AWS-dev2/5a6d0ced-c8af-4fa3-9b24-8c5a3ea11cf8",
            "securityConfiguration": {
                "enabled": false
            },
            "creationDate": "2018-06-01T13:14:43.530000+00:00",
            "crn": "crn:altus:analyticdb:us-west-1:12a0079b-1591-4ca0-b721-a446bda74e67:cluster:spot/70595482-6a46-4a9d-b395-56fcabe079e4",
            "instanceType": "r4.4xlarge",
            "cdhVersion": "CDH514"
        },
      ...
    ]
    """
    return _exec('analyticdb', 'listClusters')

  def submit_hue_query(self, cluster_crn, payload):
    return _exec('analyticdb', 'submitHueQuery', {'clusterCrn': cluster_crn, 'payload': payload})
