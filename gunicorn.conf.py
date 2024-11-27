# Gunicorn configuration file:
# https://docs.gunicorn.org/en/stable/configure.html
# https://docs.gunicorn.org/en/stable/settings.html
# Note: The classic Python buildpack currently sets a few gunicorn settings automatically via
# the `GUNICORN_CMD_ARGS` env var (which take priority over the settings in this file):
# https://github.com/heroku/heroku-buildpack-python/blob/main/vendor/python.gunicorn.sh

import os

# On Heroku, web dynos must bind to the port number specified via the `PORT` env var. This
# env var is set automatically for web dynos and also when using `heroku local` locally:
# https://devcenter.heroku.com/articles/dyno-startup-behavior#port-binding-of-web-dynos
# https://devcenter.heroku.com/articles/heroku-local
# Gunicorn will automatically use the `PORT` env var, however, by default it will bind to the
# port using the IPv4 interface (`0.0.0.0`). We configure the binding manually to make it bind
# to the IPv6 interface (`::`) instead, so that the app works in IPv6-only environments too.
# (IPv4 connections will still work so long as `IPV6_V6ONLY` hasn't been enabled.)
bind = ["[::]:{}".format(os.environ.get("PORT", 5006))]

# The default `sync` worker is more suited to CPU/network-bandwidth bound workloads, so we
# instead use the thread based worker type for improved support of blocking I/O workloads:
# https://docs.gunicorn.org/en/stable/design.html#server-model
#
# If you need to further improve the performance of blocking I/O workloads, you may want to
# try the `gevent` worker type, though you will need to disable `preload_app`, enable DB
# connecting pooling, and be aware that gevent's monkey patching can break some packages.
#
# Note: When changing the number of dynos/workers/threads you will want to make sure you
# do not exceed the maximum number of connections to external services such as DBs:
# https://devcenter.heroku.com/articles/python-concurrency-and-database-connections
worker_class = "gthread"

# gunicorn will start this many worker processes. The Python buildpack automatically sets a
# default for WEB_CONCURRENCY at dyno boot, based on the number of CPUs and available RAM:
# https://devcenter.heroku.com/articles/python-concurrency
workers = os.environ.get("WEB_CONCURRENCY", 1)

# Each `gthread` worker process will use a pool of this many threads.
threads = 5

# Load the app before the worker processes are forked, to reduce memory usage and boot times.
preload_app = True

# Workers silent for more than this many seconds are killed and restarted.
# Note: This only affects the maximum request time when using the `sync` worker.
# For all other worker types it acts only as a worker heartbeat timeout.
timeout = 20

# After receiving a restart signal, workers have this much time to finish serving requests.
# This should be set to a value less than the 30 second Heroku dyno shutdown timeout:
# https://devcenter.heroku.com/articles/dyno-shutdown-behavior
graceful_timeout = 20
