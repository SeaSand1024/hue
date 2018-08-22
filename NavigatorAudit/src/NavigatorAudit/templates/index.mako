<%!from desktop.views import commonheader, commonfooter %>
<%namespace name="shared" file="shared_components.mako" />

%if not is_embeddable:
${commonheader("Navigatoraudit", "NavigatorAudit", user, request) | n,unicode}
%endif

${shared.menubar(section='mytab')}

## Use double hashes for a mako template comment
## Main body

<div class="container-fluid">
  <div class="card">
    <h2 class="card-heading simple">
      Navigator audit ingest
    </h2>
    <p>
      The traffic example is a pipeline that retrieves measurements of traffic congestion and stores an aggregated view of the traffic congestion
      at a point in time using the current measurement and all of those in the previous 60 seconds. Within Envelope this uses the Apache Spark Streaming window
      operations functionality. This example demonstrates use cases that need to do live aggregations of recently received messages prior to user querying.
    </p>

    <h2 class="card-heading simple">
      Batch
    </h2>
    <div class="card-body">
      <p>Has Sqoop Service: ${ has_kafka_service }</p>
      <p>Has Impala: ${ has_kudu_service }</p>
      <p>Has table <a class="button">Create</a></p>
    </div>

    <h2 class="card-heading simple">
      Live
    </h2>
    <div class="card-body">
      <p>Has Kafka Service: ${ has_kafka_service }</p>
      <p>Has Kafka traffic topic: ${ has_kafka_topic } <a class="button">Create</a></p>
      <p>Has Kudu: ${ has_kudu_service }</p>
      <p>Has table <a class="button">Create</a></p>
    </div>
  </div>
</div>

%if not is_embeddable:
${commonfooter(request, messages) | n,unicode}
%endif
