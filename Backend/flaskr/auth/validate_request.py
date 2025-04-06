from flask import request,jsonify
from .jwt import validate_session
from .roles import has_admin_rights


def _check_valid_session_in_request(request):
    if 'Session' not in request.cookies:
        return jsonify({"error": "Unauthorized."}), 403

    session = request.cookies.get('Session')
    j = validate_session(session) 
    if not j:
        return jsonify({"error": "Unauthorized."}), 403
    return j


def validate_admin_request(request):
    """
    validate if the sender of this request has admin rights or not
    
    returns None if satisfied, otherwise 403 respone
    """
    r = _check_valid_session_in_request(request)
    if type(r) is tuple:
        return r

    if not has_admin_rights(r['aud']):
        return jsonify({"error": "Unauthorized."}), 403

    # return nothing if all checks passed
