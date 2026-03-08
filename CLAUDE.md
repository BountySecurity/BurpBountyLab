# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Burp Bounty Lab is an **intentionally vulnerable** Flask web application designed for testing [Burp Bounty Pro](https://bountysecurity.ai/pages/burp-bounty) scanner profiles. It simulates a wide range of vulnerability classes (XSS, SQLi, RCE, SSRF, SSTI, XXE, etc.) plus product-specific endpoints (WordPress, Spring Boot, Drupal, Jira, Confluence, etc.) so that Burp Bounty detection profiles can be validated against known-vulnerable targets.

**WARNING:** This application is intentionally insecure. Never expose it to the internet.

## Build & Run

```bash
# Build and run with Docker Compose (exposes on port 8088)
docker compose up --build

# Or build/run directly
docker build -t vulnapp .
docker run -p 8088:8088 vulnapp
```

The app listens on port 8088 both inside the container and on the host. No tests or linter are configured.

## Architecture

- **`app.py`** — Flask entrypoint. Registers all vulnerability module blueprints. Configures SECRET_KEY, DB_PATH, and FAKE_WIN_INI paths.
- **`modules/`** — Each file is a self-contained Flask Blueprint implementing one vulnerability category:
  - `xss.py`, `sqli.py`, `rce.py`, `path_traversal.py`, `ssrf.py`, `redirect.py`, `cors.py`, `crlf.py`, `ssti.py`, `xxe.py` — Core OWASP vulnerability classes
  - `graphql_vuln.py` — GraphQL introspection and query injection
  - `cves.py` — Simulated CVE endpoints for Jira, Confluence, Grafana, FortiOS, Spring Cloud, Apache, Tomcat, WebLogic, etc.
  - `wordpress.py`, `spring.py`, `drupal.py` — Product-specific vulnerability simulations
  - `passive_triggers.py` — Endpoints that trigger passive scanner detections (leaked secrets, insecure cookies, missing headers, tech fingerprints)
  - `collaborator.py` — Header injection endpoints for Burp Collaborator-style testing
  - `misc.py` — Source disclosure, exposed .git/.svn, Swagger, DWR endpoints
  - `index.py` — Landing page with links to all endpoints
- **`templates/`** — Currently empty; HTML is rendered inline via `render_template_string`.
- **`static/`** — Logo images (Logo_pro.jpg, BountySecurity_Logo.png) served by Flask for the landing page.
- **`files/`** — Static files served by the path traversal module (readme.txt, config.txt, home/).
- **`Dockerfile`** — Sets up fake `/etc/passwd`, `win.ini`, `.git/`, `.svn/` fixtures and initializes a SQLite database (`vuln.db`) with `users` and `products` tables.

## Adding a New Vulnerability Module

1. Create `modules/<name>.py` with a Flask `Blueprint` (use a unique `url_prefix`).
2. Import and register the blueprint in `app.py`.
3. Add links to the new endpoints in the `INDEX_HTML` string in `modules/index.py`.

## Key Conventions

- Each vulnerability endpoint is deliberately insecure — user input is reflected/executed without sanitization. This is by design.
- Endpoints document which Burp Bounty profiles they trigger via docstrings.
- The SQLite database at `/app/vuln.db` is initialized in the Dockerfile (not at runtime).
- Dependencies: Flask, requests, lxml, graphql-core, Jinja2 (see `requirements.txt`).
