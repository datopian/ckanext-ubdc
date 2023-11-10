from ckan import model
from ckan.logic import get_action
import ckan.plugins.toolkit as tk
from ckanext.ubdc import view


def popular_datasets(limit=3):
    """Return a list of the most popular datasets."""
    context = {"model": model, "session": model.Session}
    data_dict = {"sort": "views_recent desc", "rows": limit}
    return get_action("package_search")(context, data_dict)["results"]


def resources_count():
    """Return the total number of resources."""
    context = {"model": model, "session": model.Session}
    data_dict = {"query": "name:"}
    return get_action("resource_search")(context, data_dict)["count"]


def tags_count():
    """Return the total number of tags."""
    context = {"model": model, "session": model.Session}
    return {"count": len(get_action("tag_list")(context, {}))}


def get_gtm_id():
    """Return the Google Tag Manager ID."""
    return tk.config.get("ls", "")


def get_cookie_control_config():
    cookie_control_config = {}

    api_key = tk.config.get("ckanext.ubdc.cc.api_key", "")
    cookie_control_config["api_key"] = api_key

    license_type = tk.config.get("ckanext.ubdc.cc.license_type", "COMMUNITY")
    cookie_control_config["license_type"] = license_type

    popup_position = tk.config.get("ckanext.ubdc.cc.popup_position", "LEFT")
    cookie_control_config["popup_position"] = popup_position

    theme_color = tk.config.get("ckanext.ubdc.cc.theme_color", "DARK")
    cookie_control_config["theme_color"] = theme_color

    initial_state = tk.config.get("ckanext.ubdc.cc.initial_state", "OPEN")
    cookie_control_config["initial_state"] = initial_state

    gtm_id = tk.config.get("googleanalytics.measurement_id", "")
    cookie_control_config["gtm_id"] = gtm_id.replace("G-", "_ga_")

    return cookie_control_config


def get_field_to_question(value):
    get_field_to_question = {
        "first_name": "First Name",
        "surname": "Surname",
        "organization": "Organisation / Institution",
        "email": "Email Address",
        "telephone": "Telephone Number",
        "country": "Country",
        "summary_of_project": "Summary of your project or intended use of UBDC data and/or services",
        "project_funding": "The UBDC does not provide project funding itself, but our collections and services can be used in projects funded from other sources. Are you applying for funding for this project or work?",
        "funding_information": "If yes, please provide additional information (e.g. deadline) and/or a link to the Funding Call.",
        "wish_to_use_data": "Please select all data from the UBDC collections you wish to use.",
        "document_url": "Optional supporting documentation upload (PDF or DOC only).",
        "created": "Date of submission",
    }
    return get_field_to_question.get(value, value)
