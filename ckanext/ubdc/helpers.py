from ckan import model
from ckan.logic import get_action
import ckan.plugins.toolkit as tk
from ckanext.ubdc import view
from ckanext.googleanalytics.dbutil import get_top_packages
import ckan.lib.dictization.model_dictize as model_dictize
import ckan.lib.helpers as h
import logging

log = logging.getLogger(__name__)

from cachetools import cached
from cachetools import TTLCache

cache_time = tk.config.get("ckanext.stats.cache_time", 120)


@cached(cache=TTLCache(maxsize=1024, ttl=cache_time))
def popular_datasets(limit=3):
    """Return a list of the most popular datasets."""
    packages = get_top_packages(limit)
    context = {"model": model, "session": model.Session}
    datasets = [
        model_dictize.package_dictize(dataset[0], context) for dataset in packages
    ]
    return datasets


@cached(cache=TTLCache(maxsize=1024, ttl=cache_time))
def latest_datasets(limit=3):
    """Return a list of the most popular datasets."""
    context = {"model": model, "session": model.Session}
    data_dict = {"sort": "metadata_created desc", "rows": limit}
    packages = get_action("package_search")(context, data_dict)
    return packages.get("results", [])


@cached(cache=TTLCache(maxsize=1024, ttl=cache_time))
def resources_count():
    """Return the total number of resources."""
    context = {"model": model, "session": model.Session}
    data_dict = {"query": "name:"}
    return get_action("resource_search")(context, data_dict)["count"]


@cached(cache=TTLCache(maxsize=1024, ttl=cache_time))
def tags_count():
    """Return the total number of tags."""
    context = {"model": model, "session": model.Session}
    return {"count": len(get_action("tag_list")(context, {}))}


def get_gtm_id():
    """Return the Google Tag Manager ID."""
    return tk.config.get("ckanext.ubdc.gtm_id", "")


def get_newsletter_link():
    """Return the Newsletter Link."""
    return tk.config.get("ckanext.ubdc.newsletter_link", "")


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
        "contact_consent": "Contact Consent",
    }
    return get_field_to_question.get(value, value)


@cached(cache=TTLCache(maxsize=1024, ttl=86400))
def get_data_providers():
    # Get the data provider only when they have the image to show on homepage
    group_list = []
    try:

        context = {"model": model, "session": model.Session}
        groups = (
            model.Session.query(model.Group)
            .filter(model.Group.image_url != "")
            .filter(model.Group.type == "organization")
            .filter_by(state="active")
            .all()
        )
        group_list = model_dictize.group_list_dictize(groups, context)
    except:
        # Fallback to get_featured_organizations which already exists
        group_list = []
        limit = tk.config.get("organization_list_size_homepage", 50)
        group_list = h.get_featured_organizations(limit)

    return group_list


@cached(cache=TTLCache(maxsize=1024, ttl=86400))
def get_featured_groups(size=10):
    # Get the data provider only when they have the image to show on homepage
    group_list = []
    try:

        context = {"model": model, "session": model.Session}
        group_list = get_action("group_list")(
            context, {"all_fields": True, "limit": size}
        )
    except:
        # Fallback to get_featured_organizations which already exists
        group_list = []
        limit = tk.config.get("organization_list_size_homepage", 50)
        group_list = h.get_featured_organizations(limit)

    return group_list
