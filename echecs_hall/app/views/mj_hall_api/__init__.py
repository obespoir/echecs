#!/usr/bin/env python
# coding=utf-8
from app.extensions.blueprint import Blueprint
mj_hall = Blueprint('mj_hall', url_prefix="/majapi")

import app.views.mj_hall_api.login_hall
import app.views.mj_hall_api.email
import app.views.mj_hall_api.good
import app.views.mj_hall_api.personal
import app.views.mj_hall_api.income_support
import app.views.mj_hall_api.user_info

