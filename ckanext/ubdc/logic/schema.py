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
list_of_strings = toolkit.get_validator("list_of_strings")


def request_data_access_base_schema():
    schema = {
        "id": [ignore_missing],
        "first_name": [not_empty, unicode_safe],
        "surname": [not_empty, unicode_safe],
        "organization": [not_empty, unicode_safe],
        "email": [not_empty, unicode_safe],
        "country": [not_empty, unicode_safe],
        "summary_of_project": [not_empty, unicode_safe],
        "project_funding": [not_empty, unicode_safe, boolean_validator],
        "funding_information": [ignore_missing, unicode_safe],
        "wish_to_use_data": [ignore_missing, list_of_strings],
        "document_url": [ignore_missing, unicode_safe],
        "deleted": [ignore_missing],
    }
    return schema


def request_data_access_schema():
    return request_data_access_base_schema()
