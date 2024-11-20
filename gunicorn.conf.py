# Gunicorn configuration file:
# https://docs.gunicorn.org/en/stable/configure.html
# https://docs.gunicorn.org/en/stable/settings.html
# Note: The classic Python buildpack currently sets a few gunicorn settings automatically via
# the `GUNICORN_CMD_ARGS` env var (which take priority over the settings in this file):
# https://github.com/heroku/heroku-buildpack-python/blob/main/vendor/python.gunicorn.sh

import os

# The `PORT` env var is set automatically for web dynos and when using `heroku local`:
# https://devcenter.heroku.com/articles/dyno-startup-behavior#port-binding-of-web-dynos
# https://devcenter.heroku.com/articles/heroku-local
_port = os.environ.get("PORT", 5006)
# Bind to the IPv6 interface instead of the gunicorn default of IPv4, so the app works in IPv6-only
# environments. IPv4 connections will still work so long as `IPV6_V6ONLY` hasn't been enabled.
bind = [f"[::]:{_port}"]
