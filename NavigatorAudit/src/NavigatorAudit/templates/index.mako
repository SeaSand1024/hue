<%!from desktop.views import commonheader, commonfooter %>
<%namespace name="shared" file="shared_components.mako" />

%if not is_embeddable:
${commonheader("Navigatoraudit", "NavigatorAudit", user, request) | n,unicode}
%endif

${shared.menubar(section='mytab')}


<div class="container-fluid">
  <div class="card">
    <h2 class="card-heading simple">
      Navigator Audit Ingest
    </h2>
    <p>
Cloudera Navigator Audit is a tool that collects and consolidates audit records from several Hadoop services.
It offers the ability to forward those events into a Kafka topic for downstream consumption.

This example reads audit events from a Kafka topic populated by Navigator Audit and writes them to Kudu and Solr. 
We have also added a batch export from Navigator Database to a partitioned table on HDFS filesystem.
    </p>

    <h2 class="card-heading simple">
      Live (Kudu SQL)
    </h2>
    <div class="card-body">
      <p>Has Kafka Service: ${ has_kafka_service }</p>
      <p>Has Kafka traffic topic: ${ has_kafka_topic } <a class="button">Create</a></p>
      <p>Has Kudu: ${ has_kudu_service }</p>
      <p>Has table <a class="button">Create</a></p>
    </div>
    
    <h2 class="card-heading simple">
      Live (Solr)
    </h2>
    <div class="card-body">
      <p>Has Kafka Service: ${ has_kafka_service }</p>
      <p>Has Kafka traffic topic: ${ has_kafka_topic } <a class="button">Create</a></p>
      <p>Has Solr: ${ has_kudu_service }</p>
      <p>Has collection <a class="button">Create</a></p>
    </div>
    
    <h2 class="card-heading simple">
      Batch (Sqoop to HDFS)
    </h2>
    <div class="card-body">
      <p>Has Sqoop Service: ${ has_kafka_service }</p>
      <p>Has Impala: ${ has_kudu_service }</p>
      <p>Has table <a class="button">Create</a></p>
    </div>
  </div>
</div>

%if not is_embeddable:
${commonfooter(request, messages) | n,unicode}
%endif
