
from ckan import model
from ckan.logic import get_action
import ckan.plugins.toolkit as tk

def popular_datasets(limit=3):
    """Return a list of the most popular datasets."""
    context = {'model': model, 'session': model.Session}
    data_dict = {'sort': 'views_recent desc', 'rows': limit}
    return get_action('package_search')(context, data_dict)['results']          


def resources_count():
    """Return the total number of resources."""
    context = {'model': model, 'session': model.Session}
    data_dict = {'query': 'name:'}
    return get_action('resource_search')(context, data_dict)['count']

def tags_count():
    """Return the total number of tags."""
    context = {'model': model, 'session': model.Session}
    return {'count': len(get_action('tag_list')(context, {})) }

def get_gtm_id():
    """Return the Google Tag Manager ID."""
    return tk.config.get('ls', '')

def get_cookie_control_config():

        cookie_control_config = {}

        api_key = tk.config.get(
            'ckanext.nhs.cc.api_key', '')
        cookie_control_config['api_key'] = api_key

        license_type = tk.config.get(
            'ckanext.nhs.cc.license_type', 'COMMUNITY')
        cookie_control_config['license_type'] = license_type

        popup_position = tk.config.get(
            'ckanext.nhs.cc.popup_position', 'LEFT')
        cookie_control_config['popup_position'] = popup_position

        theme_color = tk.config.get(
            'ckanext.nhs.cc.theme_color', 'DARK')
        cookie_control_config['theme_color'] = theme_color

        initial_state = tk.config.get(
            'ckanext.nhs.cc.initial_state', 'OPEN')
        cookie_control_config['initial_state'] = initial_state

        gtm_id = tk.config.get(
             'googleanalytics.measurement_id', '')
        cookie_control_config['gtm_id'] = gtm_id.replace('G-', '_ga_')

        return cookie_control_config
