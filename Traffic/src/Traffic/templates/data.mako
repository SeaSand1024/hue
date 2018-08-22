<%!from desktop.views import commonheader, commonfooter %>
<%namespace name="shared" file="shared_components.mako" />

%if not is_embeddable:
${commonheader("Traffic", "Traffic", user, request) | n,unicode}
%endif

${shared.menubar(section='data')}


<div class="container-fluid">
  <div class="card">    
    <h2 class="card-heading simple">
      Checklist
    </h2>
    <div class="card-body">
      <p>Is generating data: ?</p>
      <p>Is ingesting data: ?</p>
    </div>
  </div>
</div>

%if not is_embeddable:
${commonfooter(request, messages) | n,unicode}
%endif
