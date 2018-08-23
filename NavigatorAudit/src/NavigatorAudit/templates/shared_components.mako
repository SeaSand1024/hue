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
              <a href="/NavigatorAudit">
                <img src="${ static('NavigatorAudit/art/icon_NavigatorAudit_48.png') }" class="app-icon"  alt="${ _('App icon') }"/>
                Navigator Audit
              </a>
             </li>
             <li class="${is_selected(section, 'mytab')}"><a href="#">Setup</a></li>
             <li class="${is_selected(section, 'mytab2')}"><a href="#">Tab 2</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</%def>
