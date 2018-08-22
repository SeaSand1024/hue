<%!from desktop.views import commonheader, commonfooter %>
<%namespace name="shared" file="shared_components.mako" />

%if not is_embeddable:
${commonheader("Altusdemo", "AltusDemo", user, request) | n,unicode}
%endif

${shared.menubar(section='mytab')}

## Use double hashes for a mako template comment
## Main body

<div class="container-fluid">
  <div class="card">
    <h2 class="card-heading simple">Altusdemo app is successfully setup!</h2>
    <div class="card-body">
      <p>It's now ${date}.</p>
    </div>
  </div>
</div>
%if not is_embeddable:
${commonfooter(request, messages) | n,unicode}
%endif
