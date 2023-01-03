import json
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.ubdc.helpers as helpers

class UbdcPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets', 'ubdc')
    
    # IPackageController
    def before_index(self, data_dict):
        if data_dict.get('data_schema', False):
            # convert the dict to json
            data_dict['data_schema'] = json.dumps(data_dict['data_fields'])
        return data_dict
            

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'popular_datasets': helpers.popular_datasets,
            'resources_count': helpers.resources_count,
            'tags_count': helpers.tags_count,
        }