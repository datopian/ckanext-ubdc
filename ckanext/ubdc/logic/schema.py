import ckan.plugins.toolkit as toolkit

if toolkit.check_ckan_version("2.10"):
    unicode_safe = toolkit.get_validator("unicode_safe")
else:
    unicode_safe = str

not_empty = toolkit.get_validator("not_empty")
empty = toolkit.get_validator("empty")
if_empty_same_as = toolkit.get_validator("if_empty_same_as")
ignore_missing = toolkit.get_validator("ignore_missing")
ignore = toolkit.get_validator("ignore")
keep_extras = toolkit.get_validator("keep_extras")
boolean_validator = toolkit.get_validator("boolean_validator")
convert_to_list_if_string = toolkit.get_validator("convert_to_list_if_string")


def request_data_access_base_schema():
    schema = {
        "id": [ignore_missing],
        "fullname": [not_empty, unicode_safe],
        "organization": [not_empty, unicode_safe],
        "email": [not_empty, unicode_safe],
        "telephone": [not_empty, unicode_safe],
        "postal_address": [not_empty, unicode_safe],
        "summary_of_project": [not_empty, unicode_safe],
        "project_funding": [not_empty, unicode_safe, boolean_validator],
        "additional_funding_information": [ignore, unicode_safe],
        "wish_to_use_data": [ignore_missing, unicode_safe, convert_to_list_if_string],
        "suggest_data": [ignore_missing, unicode_safe],
        "collaborate": [ignore_missing, unicode_safe],
        "document_url": [ignore_missing, unicode_safe],
        "deleted": [ignore_missing],
    }
    return schema


def request_data_access_schema():
    return request_data_access_base_schema()
