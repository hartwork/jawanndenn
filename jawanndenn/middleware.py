# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from functools import wraps


def set_remote_addr_to_x_forwarded_for(get_response):
    """
    Allow use of rate limiting key "ip" and "user_or_ip"
    (that looks at header REMOTE_ADDR) from behind a reverse proxy.

    For more details:
    https://django-ratelimit.readthedocs.io/en/latest/security.html#middleware
    """

    @wraps(get_response)
    def process_request(request):
        try:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            pass

        return get_response(request)

    return process_request
