import ast
import datetime
import logging
import ckan.plugins.toolkit as tk
from ckan.lib.navl.dictization_functions import validate
import ckan.lib.uploader as uploader
from ckan.lib.mailer import mail_recipient
from ckanext.ubdc.logic import schema
from ckanext.ubdc.model.access_request import RequestDataAccess

log = logging.getLogger(__name__)


def _access_request_notification(request_id):
    """
    Send notification to admin when a new data access request is submitted
    """
    site_title = tk.config.get("ckan.site_title")
    site_url = tk.config.get("ckan.site_url")
    datetime_now = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")

    body_html = f"""
    <p>Dear Admin,</p>
    <p>A new submission from the Access Our Services form has been received.</p>
    <p>Please check <a href='{site_url}/data-service/access-request/view/{request_id}'>here</a> to action the request.</p>
    <p>The data request was submitted on {datetime_now}.</p>
    
    <p></p>
    <p>Have a nice day.<p>

    <p>--<p>
    <p>Message sent by {site_title} ({site_url})</p>
    <p>This is an automated message, please don't respond to this address.</p>
    """

    subject = "New Data Services Enquiry Submitted"
    emails = tk.config.get(
        "ckanext.ubdc.access_request_email_notification_email_to", ""
    )

    for email in emails.split(" "):
        try:
            mail_recipient("", email, subject, body="", body_html=body_html)
            log.info(f"Email sent to {email} for new data access request")
        except Exception as e:
            log.error(f"Error sending email to {email} for new data access request")
            log.error(e)


def request_data_access_create(context, data_dict):
    """
    Data access request action
    :param first_name: first name
    :param surname: surname
    :param organization: organisation/institution name
    :param email: email address
    :param country: country
    :param summary_of_project: project or intended use of data
    :param project_funding: project funding
    :param funding_information: additional funding information
    :param wish_to_use_data: wish to use data
    :param supporting_doc: supporting doc file upload
    """

    if not context.get("for_view", False):
        tk.check_access("request_data_access_create", context, data_dict)

    upload = uploader.get_uploader("forms")

    upload.update_data_dict(
        data_dict, "document_url", "document_upload", "clear_upload"
    )

    data_dict, errors = validate(
        data_dict, schema.request_data_access_base_schema(), context
    )

    if errors:
        raise tk.ValidationError(errors)

    upload.upload(10)

    data = RequestDataAccess.create(data_dict)
    _access_request_notification(data.id)
    return data.as_dict()


def request_data_access_update(context, data_dict):
    """
    Data access request update action
    """
    tk.get_or_bust(data_dict, "id")

    upload = uploader.get_uploader("forms")

    tk.check_access("request_data_access_update", context, data_dict)

    upload.update_data_dict(
        data_dict, "document_url", "document_upload", "clear_upload"
    )

    data_dict, errors = validate(
        data_dict, schema.request_data_access_base_schema(), context
    )

    if errors:
        raise tk.ValidationError(errors)

    upload.upload(10)

    data = RequestDataAccess.update(data_dict)
    return data.as_dict()


def request_data_access_delete(context, data_dict):
    """
    Data access request delete action
    """
    tk.check_access("request_data_access_update", context, data_dict)
    tk.get_or_bust(data_dict, "id")
    RequestDataAccess.delete(data_dict["id"])
    return {"success": True}


@tk.side_effect_free
def request_data_access_list(context, data_dict):
    """
    Get all data access requests
    """
    tk.check_access("request_data_access_list", context, data_dict)
    data_dict = [item.as_dict() for item in RequestDataAccess.get_all()]
    return data_dict


@tk.side_effect_free
def request_data_access_show(context, data_dict):
    """
    Get data access request by id
    """
    tk.get_or_bust(data_dict, "id")
    tk.check_access("request_data_access_show", context, data_dict)

    data_dict = RequestDataAccess.get_by_id(data_dict["id"])
    return data_dict.as_dict()
