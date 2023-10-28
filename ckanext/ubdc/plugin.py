import json
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.ubdc.helpers as helpers
from ckan.lib.plugins import DefaultTranslation
from ckanext.ubdc.view import get_blueprints
from ckanext.ubdc.validators import resource_type_validator


class UbdcPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "ubdc")

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator("ignore_missing")
        schema.update(
            {
                "ckanext.ubdc.gtm_id": [ignore_missing],
            }
        )
        return schema

    # IPackageController
    def before_index(self, data_dict):
        if data_dict.get("data_schema", False):
            # convert the dict to json
            data_dict["data_schema"] = json.dumps(data_dict["data_schema"])
        return data_dict

    # ITemplateHelpers
    def get_helpers(self):
        return {
            "popular_datasets": helpers.popular_datasets,
            "resources_count": helpers.resources_count,
            "tags_count": helpers.tags_count,
            "get_gtm_id": helpers.get_gtm_id,
            "get_cookie_control_config": helpers.get_cookie_control_config,
        }

    # IValidators
    def get_validators(self):
        return {
            "resource_type_validator": resource_type_validator,
        }

    # IBlueprint
    def get_blueprint(self):
        return get_blueprints()
