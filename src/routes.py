# main/routes.py
from flask import request

from . import main
from .services import getLRTTotalSupply,getLRTCirculationAmount,getClaimedTokenByPlanId,getUnlockedTeamToken,getStakingCirculation
from .utils.cache_middleware import cache_request
from .utils.required_params import require_params
from .utils.handle_exceptions import handle_exceptions

@main.route('/')
def index():
  return "hello landRocker"

@main.route('/lrt-total-supply')
@handle_exceptions
@cache_request(timeout=60)
def lrtTotalSupply():
    return getLRTTotalSupply()

@main.route('/lrt-circulation-amount')
@handle_exceptions
@cache_request(timeout=60)
def lrtCirculationAmount(): 
    return getLRTCirculationAmount()

@main.route('/claimed-tokens-by-planId')
@require_params('planId')
@handle_exceptions
@cache_request(timeout=600) 
def claimedTokenByPlanId():
    planId = request.args.get('planId')
    return getClaimedTokenByPlanId(planId)

@main.route('/unlocked-team-tokens')
@handle_exceptions
@cache_request(timeout=600)  # Dynamic timeout in seconds  
def unlockedTeamToken():
    return getUnlockedTeamToken()

@main.route('/staking-circulation')
@handle_exceptions
@cache_request(timeout=60)
def stakingCirculation():
    return getStakingCirculation()