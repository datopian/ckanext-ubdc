
from ckan import model
from ckan.logic import get_action


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