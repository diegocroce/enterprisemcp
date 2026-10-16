"""Seed data for EnterpriseMCP. Facts from GitHub metadata (2026-10-16) and vendor docs. 'unknown' = not verified."""
import json, pathlib
from score import score
gh=json.load(open('/tmp/gh.json'))
U='unknown'
def G(repo,name,system,vendor,official,auth,rw,notes=''):
    m=gh[repo.lower()]
    return dict(name=name,system=system,maintainer=vendor,official=official,url=f'https://github.com/{repo}',repo=repo,
      auth=auth,access=rw,hosting='self-hosted',audit_logging=U,last_updated=m['last_updated'],stars=m['stars'],
      license=m['license'],archived=m['archived'],notes=notes)
def V(name,system,vendor,url,auth,rw,hosting,updated=U,notes='',lic='proprietary (vendor service)'):
    return dict(name=name,system=system,maintainer=vendor,official=True,url=url,repo=None,auth=auth,access=rw,hosting=hosting,
      audit_logging=U,last_updated=updated,stars=None,license=lic,archived=False,notes=notes)
S=[
V('Salesforce Hosted MCP Servers','Salesforce','Salesforce','https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/sobject-all.html','OAuth 2.0 (PKCE, External Client App)','read-write','hosted','2026-04','GA Apr 2026 for Enterprise Edition+; enforces org permissions. sobject-all server is full CRUD.'),
G('salesforcecli/mcp','Salesforce DX MCP Server','Salesforce','Salesforce',True,'Salesforce CLI authorized orgs','read-write','Developer-oriented (metadata, deploy, SOQL).'),
G('tsmztech/mcp-server-salesforce','Salesforce MCP Server (tsmztech)','Salesforce','tsmztech',False,U,'read-write'),
V('SAP Developer Center MCP','SAP','SAP','https://developers.sap.com/api-docs/','None (read tier) / OAuth 2.1 PKCE via SAP IAS','read-only','hosted',U,'Developer knowledge (tutorials, missions) — not business data.'),
G('cap-js/mcp-server','CAP MCP Server','SAP','SAP (cap-js)',True,'None (local dev tool)','read-only','AI-assisted development of SAP CAP apps; not a runtime data connector.'),
G('UI5/mcp-server','UI5 MCP Server','SAP','SAP (UI5)',True,'None (local dev tool)','unknown','Developer tooling for UI5.'),
G('SAP/mdk-mcp-server','MDK MCP Server','SAP','SAP',True,'None (local dev tool)','unknown','Mobile Development Kit dev tooling.'),
G('mario-andreschak/mcp-abap-adt','ABAP ADT MCP Server','SAP','mario-andreschak',False,'SAP user credentials (ADT)','read-only','Reads ABAP source/objects via ADT.'),
G('lemaiwo/btp-sap-odata-to-mcp-server','SAP OData to MCP (BTP)','SAP','lemaiwo',False,'SAP BTP (XSUAA / destinations)','read-write'),
V('Siebel AI Connectors','Oracle Siebel','Oracle','https://docs.oracle.com/en/applications/siebel/siebel-crm/26.8/szain/siebel-ai-connectors.html',U,'configurable','self-hosted or Siebel Cloud Manager','2026 (Siebel 26.8)','Exposes selected Siebel Open Integration REST APIs as MCP tools via config (FINAL_SPECIFICATION.json, MCP_CONFIG.json).'),
V('Oracle Fusion Data Intelligence MCP Server','Oracle Fusion','Oracle','https://docs.oracle.com/en/cloud/saas/analytics/26r2/fawag/oracle-fusion-data-intelligence-mcp-server.html',U,'read-only','self-hosted (downloadable)','2026 (26R2)','Analytics over Fusion data; not a transactional Fusion CX/ERP connector.'),
G('oracle/mcp','Oracle MCP Servers (OCI, DB, etc.)','Oracle Cloud / Database','Oracle',True,'OCI config / DB credentials (varies by server)','varies by server','Monorepo of multiple Oracle servers.'),
V('ServiceNow MCP Server Console','ServiceNow','ServiceNow','https://www.servicenow.com/docs/r/intelligent-experiences/mcp-platform-manager-landing.html',U,'configurable','hosted (on your instance)','2026-09-10','Admins create governed servers exposing chosen tools; endpoint /sncapps/mcp-server/mcp/. License-tier dependent.'),
G('echelon-ai-labs/servicenow-mcp','ServiceNow MCP (Echelon AI)','ServiceNow','Echelon AI Labs',False,'Basic / OAuth / API key','read-write'),
G('michaelbuckner/servicenow-mcp','ServiceNow MCP (michaelbuckner)','ServiceNow','michaelbuckner',False,U,U),
V('Dynamics 365 Sales MCP Server','Microsoft Dynamics','Microsoft','https://learn.microsoft.com/en-us/dynamics365/sales/connect-to-model-context-protocol-sales','Microsoft Entra ID','read-write','hosted',U,'Sales agent tools; pair with Dataverse MCP for CRUD. Claude Desktop not supported per docs.'),
V('Business Central MCP Server','Microsoft Dynamics','Microsoft','https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/ai/configure-mcp-server','Microsoft Entra ID','configurable (read-only default)','hosted',U,'Create/modify/delete must be explicitly enabled per API object.'),
G('microsoft/Dataverse-MCP','Dataverse MCP (labs)','Microsoft Dynamics','Microsoft',True,'Microsoft Entra ID','read-write','Labs repo for the Dataverse remote MCP server (endpoint https://<org>.crm.dynamics.com/api/mcp).'),
G('srikanth-paladugula/mcp-dynamics365-server','MCP Dynamics 365 Server','Microsoft Dynamics','srikanth-paladugula',False,'Azure AD app (client credentials)','read-write'),
G('microsoft/mcp','Microsoft MCP catalog','Microsoft (Azure / M365)','Microsoft',True,'Microsoft Entra ID (varies)','varies by server'),
G('pnp/cli-microsoft365-mcp-server','CLI for Microsoft 365 MCP','Microsoft (Azure / M365)','PnP community',False,'Microsoft Entra ID (via CLI for M365)','read-write'),
V('Workday MCP','Workday','Workday','https://doc.workday.com/admin-guide/en-us/workday-ai/agents/external-agents/connect-an-external-agent-with-workday-mcp.html','OAuth (registered external agent)','configurable (security policies)','hosted','2026-10-09','Extend Professionals only per docs.'),
G('CDataSoftware/workday-mcp-server-by-cdata','Workday MCP (CData)','Workday','CData Software',False,'CData JDBC driver credentials','read-only','Requires commercial CData JDBC driver.'),
V('HubSpot MCP Server (remote)','HubSpot','HubSpot','https://developers.hubspot.com/docs/apps/developer-platform/build-apps/integrate-with-the-remote-hubspot-mcp-server','OAuth 2.1 (PKCE)','read-write','hosted',U,'Endpoint https://mcp.hubspot.com.'),
G('HubSpot/mcp-server','HubSpot mcp-server (repo)','HubSpot','HubSpot',True,U,U,'Low-activity repo; prefer the remote server.'),
G('reminia/zendesk-mcp-server','Zendesk MCP Server (reminia)','Zendesk','reminia',False,'API token','read-write'),
G('koundinya/zd-mcp-server','Zendesk MCP Server (koundinya)','Zendesk','koundinya',False,'API token','read-write'),
V('Atlassian Rovo MCP Server (remote)','Jira / Atlassian','Atlassian','https://github.com/atlassian/atlassian-mcp-server','OAuth 2.1','read-write','hosted',gh['atlassian/atlassian-mcp-server']['last_updated'],'Jira + Confluence; respects user permissions.',lic='Apache-2.0'),
G('sooperset/mcp-atlassian','mcp-atlassian','Jira / Atlassian','sooperset',False,'API token / PAT / OAuth','read-write','Cloud and Server/Data Center.'),
G('github/github-mcp-server','GitHub MCP Server','DevOps (GitHub/GitLab)','GitHub',True,'OAuth / PAT','read-write','Remote and local; read-only mode flag.'),
G('zereight/gitlab-mcp','GitLab MCP','DevOps (GitHub/GitLab)','zereight',False,'PAT','read-write'),
G('PagerDuty/pagerduty-mcp-server','PagerDuty MCP (local)','ITSM / Incident','PagerDuty',True,'API token','read-write','Repo archived per GitHub.'),
G('ivnvxd/mcp-server-odoo','Odoo MCP Server','ERP / Order management','ivnvxd',False,'API key / user credentials','read-write'),
G('Shopify/dev-mcp' if 'shopify/dev-mcp' in gh else 'stripe/ai','Stripe MCP / AI toolkit','Payments / Commerce','Stripe',True,'API key (restricted keys)','read-write'),
G('square/square-mcp-server','Square MCP Server','Payments / Commerce','Square',True,'Access token / OAuth','read-write'),
G('awslabs/mcp','AWS MCP Servers','Cloud (AWS)','AWS Labs',True,'AWS IAM credentials','varies by server'),
G('Azure/azure-mcp','Azure MCP Server (legacy repo)','Microsoft (Azure / M365)','Microsoft',True,'Microsoft Entra ID','read-write','Archived; moved into microsoft/mcp.'),
G('makenotion/notion-mcp-server','Notion MCP Server','Collaboration','Notion',True,'Integration token / OAuth (remote)','read-write'),
G('googleapis/mcp-toolbox','MCP Toolbox for Databases','Databases','Google',True,'DB credentials / Google IAM','configurable','Supports Postgres, MySQL, Oracle, Spanner, BigQuery and more.'),
G('crystaldba/postgres-mcp','Postgres MCP Pro','Databases','Crystal DBA',False,'Connection string','configurable (restricted/unrestricted)'),
G('benborla/mcp-server-mysql','MySQL MCP Server','Databases','benborla',False,'DB credentials','read-only (default)'),
G('mongodb-js/mongodb-mcp-server','MongoDB MCP Server','Databases','MongoDB',True,'Connection string / Atlas API key','configurable (read-only flag)'),
G('redis/mcp-redis','Redis MCP Server','Databases','Redis',True,'Redis credentials','read-write'),
G('neondatabase/mcp-server-neon','Neon MCP Server','Databases','Neon',True,'OAuth / API key','read-write'),
G('ClickHouse/mcp-clickhouse','ClickHouse MCP','Databases','ClickHouse',True,'DB credentials','read-only (default)'),
G('Snowflake-Labs/mcp','Snowflake MCP Server','Databases','Snowflake Labs',True,'Snowflake credentials','configurable'),
G('motherduckdb/mcp-server-motherduck','DuckDB / MotherDuck MCP','Databases','MotherDuck',True,'MotherDuck token','configurable'),
G('elastic/mcp-server-elasticsearch','Elasticsearch MCP Server','Databases','Elastic',True,'API key','read-only'),
G('dbt-labs/dbt-mcp','dbt MCP Server','Databases','dbt Labs',True,'dbt Cloud token','read-write'),
G('modelcontextprotocol/servers-archived','Reference servers (Postgres, SQLite, etc.)','Databases','MCP project',True,'Connection string','read-only (Postgres)','Archived; not maintained.'),
]
for s in S:
    s['id']=(s['repo'] or s['name']).lower().replace('/','-').replace(' ','-').replace('(','').replace(')','').replace('.','')
    s['score'],s['score_breakdown']=score(s)
p=pathlib.Path(__file__).resolve().parents[1]/'data/servers.json'
json.dump({'generated':'2026-10-16','servers':S},open(p,'w'),indent=1)
print(len(S))
