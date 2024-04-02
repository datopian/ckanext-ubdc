import json
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.ubdc.helpers as helpers
from ckan.lib.plugins import DefaultTranslation
from ckanext.ubdc.view import get_blueprints
from ckanext.ubdc.validators import resource_type_validator
from ckanext.ubdc.logic import action
from ckanext.ubdc.logic import auth
from ckanext.ubdc.model import access_request


class UbdcPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IAuthFunctions)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "ubdc")

    def configure(self, config):
        access_request.setup()

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator("ignore_missing")
        schema.update(
            {
                "ckanext.ubdc.gtm_id": [ignore_missing],
            }
        )
        return schema

    # IActions
    def get_actions(self):
        return {
            "request_data_access_create": action.request_data_access_create,
            "request_data_access_list": action.request_data_access_list,
            "request_data_access_show": action.request_data_access_show,
            "request_data_access_update": action.request_data_access_update,
            "request_data_access_delete": action.request_data_access_delete,
        }

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
            "get_field_to_question": helpers.get_field_to_question,
            "get_data_providers": helpers.get_data_providers,
        }

    # IValidators
    def get_validators(self):
        return {
            "resource_type_validator": resource_type_validator,
        }

    # IAuthFunctions
    def get_auth_functions(self):
        return {
            "request_data_access_list": auth.request_data_access_list,
            "request_data_access_show": auth.request_data_access_show,
            "request_data_access_update": auth.request_data_access_update,
            "request_data_access_create": auth.request_data_access_create,
        }

    # IBlueprint
    def get_blueprint(self):
        return get_blueprints()
