# main/routes.py
from flask import request

from . import main
from .services import getLRTTotalSupply,getLRTCirculationAmount
from .utils.cache_middleware import cache_request
from .utils.handle_exceptions import handle_exceptions

@main.route('/')
def index():
  return "hello landRocker"

@main.route('/lrt-total-supply')
#@handle_exceptions
#@cache_request(timeout=60)
def lrtTotalSupply():
    return getLRTTotalSupply()

@main.route('/lrt-circulation-supply')
#@handle_exceptions
#@cache_request(timeout=60)
def lrtCirculationAmount(): 
    return getLRTCirculationAmount()

