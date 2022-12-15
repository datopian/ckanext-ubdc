import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.ubdc.helpers as helpers
from ckan.lib.plugins import DefaultTranslation

class UbdcPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets', 'ubdc')

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'popular_datasets': helpers.popular_datasets,
            'resources_count': helpers.resources_count,
            'tags_count': helpers.tags_count,
        }