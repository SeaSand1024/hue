## Licensed to Cloudera, Inc. under one
## or more contributor license agreements.  See the NOTICE file
## distributed with this work for additional information
## regarding copyright ownership.  Cloudera, Inc. licenses this file
## to you under the Apache License, Version 2.0 (the
## "License"); you may not use this file except in compliance
## with the License.  You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

<%!
from django.utils.translation import ugettext as _

from desktop.views import commonheader, commonfooter, _ko, commonshare
from desktop import conf
%>

<%namespace name="common_search" file="common_search.mako" />
<%namespace name="notebookKoComponents" file="/common_notebook_ko_components.mako" />
<%!
def is_selected(section, matcher):
  if section == matcher:
    return "active"
  else:
    return ""
%>

  
%if not is_embeddable:
${ commonheader(_('Dashboard'), "dashboard", user, request, "80px") | n,unicode }
${ commonshare() | n,unicode }
${ notebookKoComponents.downloadSnippetResults() }
%endif

<div id="searchComponents" class="dashboard-container dashboard-container-flex search-components">
<div class="navbar hue-title-bar nokids">
    <div class="navbar-inner">
      <div class="container-fluid">
        <div class="nav-collapse">
          <ul class="nav">
            <li class="app-header">
              <a href="/ApacheLogs">
                <img src="${ static('ApacheLogs/art/icon_ApacheLogs_48.png') }" class="app-icon"  alt="${ _('App icon') }"/>
                Apachelogs
              </a>
            </li>
            <li class="${is_selected('mytab', 'mytab2')}"><a href="${ url('apache_logs_index') }">Install</a></li>
            <li class="${is_selected('mytab1', 'mytab1')}"><a href="${ url('apache_logs_dashboard') }?is_embeddable=true">Dahsboard</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
${ common_search.page_structure(False, is_embeddable, is_report) }
</div>

%if not is_embeddable:
${ commonfooter(request, messages) | n,unicode }
%endif
