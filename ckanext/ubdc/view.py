from crypt import methods
import logging
from flask.views import MethodView
import ckan.logic as logic
from flask import Blueprint, redirect
import ckan.model as model
from ckan.common import asbool
from ckan.plugins import toolkit as tk
from ckan.views.group import register_group_plugin_rules
from ckan.views.dataset import register_dataset_plugin_rules
from ckan.views.resource import (
    register_dataset_plugin_rules as register_resource_plugin_rules,
)
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.lib.captcha as captcha

tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params


log = logging.getLogger(__name__)

ubdc = Blueprint("ubdc", __name__)

def get_path(path, query_type, toolkit):
    original_query = toolkit.request.query_string.decode("utf-8")
    if original_query:
        target_url = "/" + query_type + "/" + path + '?' + original_query
    else:
        target_url = "/" + query_type + "/"  + path
    return target_url

# Redirect organization pages to provider pages
provider = Blueprint(
    "provider",
    __name__,
    url_prefix="/providers",
    url_defaults={"group_type": "organization", "is_organization": True},
)

datasets = Blueprint(
    "datasets",
    __name__,
    url_prefix="/datasets",
    url_defaults={"package_type": "dataset"},
)

resources = Blueprint(
    "datasets_resource",
    __name__,
    url_prefix="/datasets/<id>/resource",
    url_defaults={"package_type": "dataset"},
)

researchThemes = Blueprint(
    "research-themes",
    __name__,
    url_prefix="/research-themes",
    url_defaults={"group_type": "group", "is_organization": False},
)

@ubdc.route("/organization/")
def org_redirect_root():
    return redirect("/providers")


@ubdc.route("/organization/<path:path>")
def org_redirect(path):
    url = get_path(path, 'providers', tk)
    return redirect(url)

@ubdc.route("/group/")
def group_redirect_root():
    return redirect("/research-themes")


@ubdc.route("/group/<path:path>")
def group_redirect(path):
    url = get_path(path, 'research-themes', tk)
    return redirect(url)

@ubdc.route("/dataset")
@ubdc.route("/dataset/")
def dataset_redirect_root():
    original_query = tk.request.query_string.decode("utf-8")
    if original_query:
        target_url = '/datasets' + '?' + original_query
    else:
        target_url = '/datasets'
    return redirect(target_url)


@ubdc.route("/dataset/<path:path>")
def dataset_redirect(path):
    url = get_path(path, 'datasets', tk)
    return redirect(url)


class AccessRequestController(MethodView):
    def get(self, data={}, errors={}, error_summary={}):
        extra_vars = {"data": data, "errors": errors, "error_summary": error_summary}
        return tk.render("access_form/index.html", extra_vars)

    def post(self):
        context = {"model": model, "user": tk.c.user, "auth_user_obj": tk.c.userobj}

        data_dict = clean_dict(
            dict_fns.unflatten(tuplize_dict(parse_params(tk.request.form)))
        )

        if not asbool(data_dict.get("consent", False)):
            error_msg = tk._("Please accept the terms and conditions.")
            tk.h.flash_error(error_msg)
            return self.get()

        # if not asbool(data_dict.get("contactConsent", False)):
        #     error_msg = tk._("Please accept the contact consent.")
        #     tk.h.flash_error(error_msg)
        #     return self.get()
        try:
            captcha.check_recaptcha(tk.request)
        except captcha.CaptchaError:
            error_msg = tk._("Bad Captcha. Please try again.")
            tk.h.flash_error(error_msg)
            return self.get()

        try:
            data_dict["document_upload"] = tk.request.files.get("document_upload")
            data_dict["project_funding"] = asbool(
                data_dict.get("project_funding", False)
            )
            if data_dict.get("wish_to_use_data", False):
                if not isinstance(data_dict["wish_to_use_data"], list):
                    data_dict["wish_to_use_data"] = [
                        data_dict["wish_to_use_data"],
                    ]
            context["for_view"] = True

            tk.get_action("request_data_access_create")(context, data_dict)
        except logic.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.get(data_dict, errors, error_summary)

        tk.h.flash_success(
            "Your application has been successfully submitted, we will review your request and get back to you soon"
        )

        return tk.redirect_to("ubdc.access_request")


ubdc.add_url_rule(
    "/data-service/access-request",
    view_func=AccessRequestController.as_view("access_request"),
)


def access_request_list():
    context = {"model": model, "user": tk.c.user, "auth_user_obj": tk.c.userobj}
    try:
        result = tk.get_action("request_data_access_list")(context, {})
    except logic.NotAuthorized:
        tk.abort(403, tk._("Not authorized to see this page"))

    extra_vars = {
        "data": result,
        "errors": {},
        "error_summary": {},
    }
    return tk.render("access_form/list.html", extra_vars)


def access_request_view(id):
    context = {"model": model, "user": tk.c.user, "auth_user_obj": tk.c.userobj}
    try:
        result = tk.get_action("request_data_access_show")(context, {"id": id})
    except logic.NotAuthorized:
        tk.abort(403, tk._("Not authorized to see this page"))

    keys_to_exclude = ["id", "updated", "deleted"]

    result = {key: value for key, value in result.items() if key not in keys_to_exclude}
    extra_vars = {
        "data": result,
        "errors": {},
        "error_summary": {},
    }
    return tk.render("access_form/view.html", extra_vars)


def access_request_delete(id):
    context = {"model": model, "user": tk.c.user, "auth_user_obj": tk.c.userobj}
    try:
        result = tk.get_action("request_data_access_delete")(context, {"id": id})
    except logic.ValidationError as e:
        tk.abort(404, e.error_dict["message"])

    tk.h.flash_success("Access request deleted")
    return tk.redirect_to("ubdc.access_request_list")

def delete_all_resources(id):
    context = {"model": model, "user": tk.c.user, "auth_user_obj": tk.c.userobj}
    data_dict = {
        "id": id
    }
    try:
        package = tk.get_action("package_show")(context, data_dict)
        for resource in package.get('resources'):
            resource_delete_dict = {
                "id": resource.get('id')
            }
            tk.get_action("resource_delete")(context, resource_delete_dict)
    except logic.NotAuthorized:
        tk.abort(403, tk._("Not authorized to see this page"))
    except logic.ValidationError as e:
        tk.abort(404, e.error_dict["message"])
    return tk.redirect_to(f'/datasets/{id}')

def cookie_policy():
    return tk.render("cookie/index.html")

ubdc.add_url_rule("/data-service/access-request/view", view_func=access_request_list)

ubdc.add_url_rule("/cookie-policy", view_func=cookie_policy)


ubdc.add_url_rule(
    "/data-service/access-request/view/<id>", view_func=access_request_view
)

ubdc.add_url_rule(
    "/data-service/access-request/view/<id>/delete",
    methods=["POST"],
    view_func=access_request_delete,
)

ubdc.add_url_rule(
    "/datasets/<id>/resource_delete_all",
    methods=["POST"],
    view_func=delete_all_resources,
)


def get_blueprints():
    register_group_plugin_rules(provider)
    register_dataset_plugin_rules(datasets)
    register_resource_plugin_rules(resources)
    register_group_plugin_rules(researchThemes)
    return [ubdc, provider, datasets, resources, researchThemes]
