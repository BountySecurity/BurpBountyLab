#!/usr/bin/env python3
"""
BurpBounty VulnApp - Vulnerable web application for testing Burp Bounty profiles.
WARNING: This is intentionally vulnerable. DO NOT expose to the internet.
"""

from flask import Flask
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = 'super-secret-key-12345'
app.config['DB_PATH'] = '/app/vuln.db'
app.config['FAKE_WIN_INI'] = '/app/fake_windows/win.ini'

# Register all vulnerability module blueprints
from modules.index import index_bp
from modules.xss import xss_bp
from modules.sqli import sqli_bp
from modules.rce import rce_bp
from modules.path_traversal import pt_bp
from modules.ssrf import ssrf_bp
from modules.redirect import redirect_bp
from modules.cors import cors_bp
from modules.crlf import crlf_bp
from modules.ssti import ssti_bp
from modules.xxe import xxe_bp
from modules.graphql_vuln import graphql_bp
from modules.cves import cves_bp
from modules.wordpress import wp_bp
from modules.spring import spring_bp
from modules.drupal import drupal_bp
from modules.misc import misc_bp
from modules.passive_triggers import passive_bp
from modules.collaborator import collab_bp
from modules.ai_endpoints import ai_bp

app.register_blueprint(index_bp)
app.register_blueprint(xss_bp)
app.register_blueprint(sqli_bp)
app.register_blueprint(rce_bp)
app.register_blueprint(pt_bp)
app.register_blueprint(ssrf_bp)
app.register_blueprint(redirect_bp)
app.register_blueprint(cors_bp)
app.register_blueprint(crlf_bp)
app.register_blueprint(ssti_bp)
app.register_blueprint(xxe_bp)
app.register_blueprint(graphql_bp)
app.register_blueprint(cves_bp)
app.register_blueprint(wp_bp)
app.register_blueprint(spring_bp)
app.register_blueprint(drupal_bp)
app.register_blueprint(misc_bp)
app.register_blueprint(passive_bp)
app.register_blueprint(collab_bp)
app.register_blueprint(ai_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088, debug=False)
