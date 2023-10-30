import ckan.plugins.toolkit as tk

Invalid = tk.Invalid
_ = tk._


def resource_type_validator(value, context):
    if value not in ["data_and_metadata", "resource"]:
        raise Invalid(
            _('Resource type must be either "data_and_metadata" or "resource"')
        )
    return value
