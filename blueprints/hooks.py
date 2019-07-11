from flask import Blueprint, request
from gzip import compress


bp = Blueprint('hooks', __name__)


# TODO: apply some security from docs (http://flask.pocoo.org/docs/1.0/security/)
@bp.after_app_request
def after_request(response):
    is_already_compressed = 'Content-Encoding' in response.headers
    # default MTU is 1500, so no need to compress a singe unit
    is_too_small = len(response.get_data()) <= 1500
    # no need to compress error responses, because they are relatively small
    is_successful = response.status_code >= 200 or response.status_code < 300
    is_json = response.content_type == 'application/json'
    # use gzip only if client can accept it
    is_gzip_allowed = 'gzip' in request.headers.get('Accept-Encoding', '').lower()

    if is_already_compressed or is_too_small or not (is_successful and is_json and is_gzip_allowed):
        return response

    # apply gzip compression
    response.set_data(compress(response.get_data()))
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Length'] = len(response.get_data())

    return response