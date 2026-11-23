"""Requests to other machines go through this one function.

A redirect is followed only to an address that is read over https. A request that carries a
key or a token is not sent on to another host, so that a redirect cannot hand the secret to
someone else.
"""

from __future__ import annotations

import urllib.request
from urllib.parse import urlsplit


class _CarefulRedirects(urllib.request.HTTPRedirectHandler):
    """Follows a redirect only when it is safe to send the same request to the new address."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old, new = urlsplit(req.full_url), urlsplit(newurl)
        names = {name.lower() for name in (*req.headers, *req.unredirected_hdrs)}
        if new.scheme != "https" or ("authorization" in names and new.hostname != old.hostname):
            return None  # the redirect itself is then reported as the answer
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_CarefulRedirects)


def open_request(request: urllib.request.Request, seconds: float):
    """Send one request and return the response."""
    return _OPENER.open(request, timeout=seconds)
