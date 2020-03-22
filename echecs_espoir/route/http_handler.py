# coding=utf-8
"""
author = jamon
"""

from aiohttp import web

from obespoir.httpserver.route import HttpHandler
from obespoir.server.server import Server


@HttpHandler("/")
async def index(request):
    return web.Response(body="hello", content_type="text/html")


@HttpHandler("/update_remote_rpc_config")
async def update_remote_rpc_config(request):
    await Server().update_remote_rpc_config()
    return web.Response(body="ok~", content_type="text/html")