<%!
from django.utils.translation import ugettext as _
%>

<%!
def is_selected(section, matcher):
  if section == matcher:
    return "active"
  else:
    return ""
%>

<%def name="menubar(section='')">
  <div class="navbar hue-title-bar nokids">
    <div class="navbar-inner">
      <div class="container-fluid">
        <div class="nav-collapse">
          <ul class="nav">
            <li class="app-header">
              <a href="/Traffic">
                <img src="${ static('Traffic/art/icon_Traffic_48.png') }" class="app-icon"  alt="${ _('App icon') }"/>
                Traffic
              </a>
             </li>
             <li class="${is_selected(section, 'mytab')}"><a href="#">Install</a></li>
             <li class="${is_selected(section, 'data')}"><a href="${ url('traffic_data') }">Data</a></li>
             <li class="${is_selected(section, 'mytab2')}"><a href="#">Query</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</%def>
