from flask import Blueprint, render_template_string

index_bp = Blueprint('index', __name__)

INDEX_HTML = """<!DOCTYPE html>
<html>
<head><title>Burp Bounty Lab</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', Arial, sans-serif; background: #f0f4f8; color: #1a1a1a; }
.header {
    background: linear-gradient(135deg, #044E71 0%, #0075A9 100%);
    padding: 30px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 20px rgba(4,78,113,0.3);
}
.header-left { display: flex; align-items: center; gap: 24px; }
.header-left img { height: 54px; }
.header-right img { height: 40px; opacity: 0.9; }
.header h1 { color: #ffffff; font-size: 1.6em; font-weight: 600; letter-spacing: 0.5px; }
.container { max-width: 1200px; margin: 0 auto; padding: 30px 40px; }
.warn {
    color: #fff;
    font-weight: 600;
    background: linear-gradient(135deg, #b33a00, #cc4400);
    padding: 14px 20px;
    border-radius: 8px;
    margin-bottom: 30px;
    font-size: 0.95em;
    text-align: center;
    box-shadow: 0 2px 8px rgba(179,58,0,0.2);
}
h2 {
    color: #ffffff;
    background: #044E71;
    padding: 12px 18px;
    border-radius: 8px 8px 0 0;
    font-size: 1.05em;
    font-weight: 600;
    letter-spacing: 0.3px;
    margin-top: 20px;
}
.section {
    margin: 0 0 20px 0;
    padding: 16px 18px;
    background: #ffffff;
    border-radius: 0 0 8px 8px;
    border: 1px solid #d0dce6;
    border-top: none;
    box-shadow: 0 2px 8px rgba(4,78,113,0.06);
}
.grid { display: flex; flex-wrap: wrap; gap: 8px; }
.section a {
    color: #044E71;
    text-decoration: none;
    display: inline-block;
    padding: 6px 14px;
    background: #e8f1f8;
    border: 1px solid #b8d4e8;
    border-radius: 6px;
    font-size: 0.9em;
    font-weight: 500;
    transition: all 0.2s ease;
}
.section a:hover {
    background: #0075A9;
    color: #ffffff;
    border-color: #0075A9;
    box-shadow: 0 2px 8px rgba(0,117,169,0.3);
}
.footer {
    text-align: center;
    padding: 24px;
    color: #6b8299;
    font-size: 0.85em;
    border-top: 1px solid #d0dce6;
    margin-top: 30px;
}
.footer a { color: #0075A9; text-decoration: none; font-weight: 500; }
.footer a:hover { text-decoration: underline; }
</style>
</head>
<body>
<div class="header">
    <div class="header-left">
        <img src="/static/Logo_pro.jpg" alt="Burp Bounty Pro">
    </div>
    <h1>Burp Bounty Lab</h1>
    <div class="header-right">
        <img src="/static/BountySecurity_Logo.png" alt="Bounty Security">
    </div>
</div>
<div class="container">
<p class="warn">WARNING: Intentionally vulnerable application for testing Burp Bounty profiles.</p>

<h2>XSS (14 profiles)</h2>
<div class="section grid">
<a href="/xss/reflect?q=test">Reflected XSS</a>
<a href="/xss/attribute?name=test">Attribute Context</a>
<a href="/xss/comment?data=test">Comment Context</a>
<a href="/xss/tag?input=test">Tag Context</a>
<a href="/xss/js?value=test">JavaScript Context</a>
<a href="/xss/url?link=http://example.com">URL Context</a>
<a href="/xss/dom?msg=test">DOM Context</a>
<a href="/xss/discover?page=1&search=test&q=hello&lang=en&keyword=foo&name=bar&redirect=no&view=default&topic=general&title=home&type=html&comment=none">XSS Discovery Params</a>
<a href="/xss/blind?feedback=test">Blind XSS (Collaborator)</a>
<a href="/xss/encoded?q=test">XSS Encoded</a>
</div>

<h2>SQL Injection (7 profiles)</h2>
<div class="section grid">
<a href="/sqli/search?q=laptop">Error-based SQLi</a>
<a href="/sqli/user?id=1">SQLi by ID</a>
<a href="/sqli/login">SQLi Login Form</a>
<a href="/sqli/time?id=1">Time-based SQLi</a>
<a href="/sqli/status?id=1">Status Code SQLi</a>
<a href="/sqli/length?q=admin">Content Length SQLi</a>
<a href="/sqli/oob?id=1">OOB SQLi (Collaborator)</a>
</div>

<h2>Remote Code Execution (13 profiles)</h2>
<div class="section grid">
<a href="/rce/ping?host=127.0.0.1">Command Injection</a>
<a href="/rce/eval?code=1%2b1">PHP-style Eval</a>
<a href="/rce/echo?input=hello">Echo RCE</a>
<a href="/rce/expect?cmd=id">Expect RCE</a>
<a href="/rce/blind?input=test">Blind RCE (Collaborator)</a>
<a href="/rce/log4j?search=test">Log4j (Collaborator)</a>
<a href="/rce/react2shell">React2Shell CVE-2025-55182</a>
</div>

<h2>Path Traversal (2 profiles + CVEs)</h2>
<div class="section grid">
<a href="/pt/read?file=readme.txt">File Read (Linux)</a>
<a href="/pt/readwin?file=config.txt">File Read (Windows)</a>
<a href="/pt/include?page=home">PHP-style Include</a>
</div>

<h2>SSRF (6 profiles)</h2>
<div class="section grid">
<a href="/ssrf/fetch?url=http://example.com">URL Fetch</a>
<a href="/ssrf/proxy?target=http://example.com">Proxy</a>
<a href="/ssrf/scheme?url=http://example.com">URL Scheme</a>
<a href="/ssrf/img?src=http://example.com/img.png">Image Proxy</a>
</div>

<h2>Open Redirect (3 profiles)</h2>
<div class="section grid">
<a href="/redirect/goto?url=/">Basic Redirect</a>
<a href="/redirect/login?next=/">Login Redirect</a>
<a href="/redirect/out?url=/">Outbound Redirect</a>
<a href="/redirect/pp?return_url=/">Parameter Pollution Redirect</a>
</div>

<h2>CORS Misconfiguration (1 profile)</h2>
<div class="section grid">
<a href="/cors/api/data">CORS API Endpoint</a>
</div>

<h2>CRLF Injection (1 profile)</h2>
<div class="section grid">
<a href="/crlf/set?lang=en">Language Setter</a>
</div>

<h2>SSTI (1 profile)</h2>
<div class="section grid">
<a href="/ssti/render?template=Hello">Template Render</a>
<a href="/ssti/preview?content=Welcome">Content Preview</a>
</div>

<h2>XXE (3 profiles)</h2>
<div class="section grid">
<a href="/xxe/parse">XML Parser</a>
<a href="/xxe/upload">XML Upload</a>
<a href="/xxe/soap">SOAP Endpoint</a>
</div>

<h2>GraphQL (6 profiles)</h2>
<div class="section grid">
<a href="/graphql">GraphQL Endpoint</a>
<a href="/graphql/ide">GraphQL IDE</a>
</div>

<h2>CVEs (42 profiles)</h2>
<div class="section grid">
<a href="/cve/jira/dashboard">Jira</a>
<a href="/cve/confluence/">Confluence</a>
<a href="/cve/grafana/">Grafana</a>
<a href="/cve/fortios/remote/login">FortiOS</a>
<a href="/cve/pulse/">Pulse Secure</a>
<a href="/cve/citrix/">Citrix</a>
<a href="/cve/f5/">F5 BigIP</a>
<a href="/cve/spring/">Spring Cloud</a>
<a href="/cve/apache/">Apache</a>
<a href="/cve/tomcat/">Tomcat</a>
<a href="/cve/weblogic/console/login/LoginForm.jsp">WebLogic</a>
<a href="/cve/cisco/">Cisco</a>
<a href="/cve/solarwinds/">SolarWinds</a>
<a href="/cve/couchdb/_all_dbs">CouchDB</a>
<a href="/cve/zoho/">ManageEngine</a>
<a href="/cve/netsweeper/">Netsweeper</a>
<a href="/cve/artica/fw.login.php">Artica</a>
<a href="/cve/ruby/">Ruby on Rails</a>
<a href="/cve/crowd/">Atlassian Crowd</a>
<a href="/cve/kubernetes/api/v1/">Kubernetes</a>
<a href="/cve/firebase/.json">Firebase</a>
<a href="/cve/magmi/">MAGMI</a>
<a href="/cve/traefik/">Traefik</a>
<a href="/cve/n8n/rest/settings">n8n</a>
<a href="/cve/symfony/profiler/phpinfo">Symfony</a>
<a href="/cve/text4shell?input=test">Text4Shell</a>
</div>

<h2>WordPress (10 profiles)</h2>
<div class="section grid">
<a href="/wp/wp-login.php">WP Login</a>
<a href="/wp/xmlrpc.php">XMLRPC</a>
<a href="/wp/wp-json/wp/v2/users">User Enum JSON</a>
<a href="/wp/wp-json/oembed/1.0/embed?url=&format=json">oEmbed</a>
<a href="/wp/author-sitemap.xml">Author Sitemap</a>
<a href="/wp/wp-config.php">WP Config</a>
<a href="/wp/wp-admin/">WP Admin Dir</a>
<a href="/wp/wp-content/">WP Content Dir</a>
<a href="/wp/wp-content/plugins/easy-wp-smtp/">Easy WP SMTP</a>
<a href="/wp/wp-content/plugins/insert-php/readme.txt">Insert PHP Plugin</a>
<a href="/wp/wp-admin/admin-ajax.php?action=duplicator_download&file=readme.txt">Duplicator</a>
</div>

<h2>Spring Boot (2 profiles)</h2>
<div class="section grid">
<a href="/actuator">Actuator Root</a>
<a href="/actuator/env">Actuator Env</a>
<a href="/actuator/health">Actuator Health</a>
<a href="/actuator/metrics">Actuator Metrics</a>
<a href="/actuator/loggers">Actuator Loggers</a>
</div>

<h2>Drupal (2 profiles)</h2>
<div class="section grid">
<a href="/drupal/admin/views/ajax/autocomplete/user/a">User Autocomplete</a>
<a href="/drupal/user/1">User Profile</a>
</div>

<h2>DWR (1 profile)</h2>
<div class="section grid">
<a href="/dwr/interface">DWR Interface</a>
<a href="/dwr/engine.js">DWR Engine</a>
</div>

<h2>Misc Discovery</h2>
<div class="section grid">
<a href="/source/test.php~">Source Code Disclosure</a>
<a href="/.git/HEAD">.git exposed</a>
<a href="/.svn/entries">.svn exposed</a>
<a href="/swagger-ui.html">Swagger UI</a>
<a href="/api/v1/status">API Endpoint</a>
</div>

<h2>Passive Detection Triggers</h2>
<div class="section grid">
<a href="/passive/secrets">Secrets in Response</a>
<a href="/passive/cookies">Insecure Cookies</a>
<a href="/passive/headers">Missing Security Headers</a>
<a href="/passive/tech">Technology Fingerprints</a>
<a href="/passive/params?id=1&user=admin&debug=true&token=abc&key=xyz&redirect_uri=http://example.com&cmd=test&file=test.txt&template=home&q=search&email=test@test.com&url=http://example.com&uuid=550e8400-e29b-41d4-a716-446655440000">Vuln Parameters</a>
<a href="/passive/api/v1/data">API Path Detection</a>
<a href="/passive/graphql">GraphQL Path Detection</a>
</div>

<h2>Header Injection (Collaborator)</h2>
<div class="section grid">
<a href="/collab/headers?param=test">X-Headers Injection</a>
<a href="/collab/host?param=test">Host Header Injection</a>
<a href="/collab/forgot?email=user@example.com">Password Reset Headers</a>
</div>

</div>
<div class="footer">
    Powered by <a href="https://bountysecurity.ai/pages/burp-bounty">Burp Bounty Pro</a> &mdash; <a href="https://bountysecurity.ai">Bounty Security</a>
</div>
</body></html>
"""

@index_bp.route('/')
def index():
    return render_template_string(INDEX_HTML)
