import logging
from flask import Blueprint, redirect

from ckan.plugins import toolkit as tk
from ckan.views.group import register_group_plugin_rules

log = logging.getLogger(__name__)

udbc = Blueprint('udbc', __name__)

# Redirect organization pages to provider pages
provider = Blueprint('provider', __name__, url_prefix='/provider', 
            url_defaults={'group_type': 'organization', 'is_organization': True})

@udbc.route('/organization/')
def org_redirect_root():
    return redirect('/provider')

@udbc.route('/organization/<path:path>')
def org_redirect(path):
    return redirect('/provider/{}'.format(path))


def get_blueprints():
    register_group_plugin_rules(provider)
    return [udbc, provider]