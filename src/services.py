# import pandas as pd
import os
from subgrounds import Subgrounds
from config import BaseConfig
from flask import jsonify # type: ignore
from config import BaseConfig
import math
from datetime import datetime
from web3 import Web3
import pandas as pd
from subgrounds.pagination import LegacyStrategy
# Instantiate the Subgrounds 
sg = Subgrounds()
pd.options.mode.chained_assignment = None
# Instantiate the config 
config = BaseConfig()

# Load 
landRocker = sg.load_subgraph(config.SUBGRAPH_URL)




def getLRTTotalSupply():
    token = landRocker.Query.tokens(
        )
    
    df = sg.query_df([
        token.totalSupply,
        token.totalMinted,
        token.totalBurnt
    ])        
    
    # Check if the DataFrame is empty
    if df.empty:
        return jsonify({"error": "No records found for the specified collection and token ID"}), 404   


    totalMint = df['tokens_totalMinted'];
    totalBurnt = df['tokens_totalBurnt'];

    df['current_supply'] = df['tokens_totalMinted'] - df['tokens_totalBurnt']  
    total_supply = int(totalMint) - int(totalBurnt)

    return jsonify(total_supply)
       
def getLRTCirculationAmount(): 
    sale_first = getClaimedTokenByPlanId("0x0")      
    sale_first = Web3.from_wei(sale_first, 'ether')  
    
    sale_second = getClaimedTokenByPlanId("0x6")      
    sale_second = Web3.from_wei(sale_second, 'ether')  

    team_first = getUnlockedTeamToken()      
    team_first = Web3.from_wei(team_first, 'ether')  

    stake = getStakingCirculation()

    uniswap_liquidity_first = 75000000
    uniswap_liquidity_second = 20000000
    mexc_liquidity_first = 30000000
    mexc_liquidity_second = 5000000
    mexc_liquidity_third = 20000000
    cls = 11880000

    
   
    total_circulation_amount = int(sale_first) + int(sale_second) + int(team_first) + int(stake) + int(uniswap_liquidity_first)+ int(uniswap_liquidity_second)+ int(mexc_liquidity_first) + int(mexc_liquidity_second) + int(mexc_liquidity_third) + int(cls)
    # total_circulation_amount = Web3.from_wei((total_circulation_amount), 'ether')  
    return jsonify(total_circulation_amount)
    # return jsonify({"total_circulation_amount": str(total_circulation_amount),"stake":str(stake), "sale_first": str(sale_first), "sale_second": str(sale_second),"team_first": str(team_first),"uniswap_liquidity": str(uniswap_liquidity),"mexci_liquidity_first": str(mexci_liquidity_first),"mexci_liquidity_second": str(mexci_liquidity_second)})
   
def getClaimedTokenByPlanId(planId):
    userVesting = landRocker.Query.userVestings(
            first=15_000,
            orderBy=landRocker.UserVesting.startDate,
            orderDirection="desc",
            where=[
                landRocker.UserVesting.plan.id == planId,
                landRocker.UserVesting.revoked == False,
            ]
        )

    df = sg.query_df([
        userVesting.vestedAmount,
        userVesting.claimedAmount,
        userVesting.startDate,
        userVesting.unlockDate,
        userVesting.endDate,
        userVesting.plan.initializeReleasePercentage
    ])

    # Check if the DataFrame is empty
    if df.empty:
        return jsonify({"error": "No records found for the specified collection and token ID"}), 404
    
    total_claimed_amount = df['userVestings_claimedAmount'].sum()
    return total_claimed_amount
    # return jsonify({"total_claimed_amount": str(total_claimed_amount)})

def getUnlockedTeamToken():
    userVestingTeams = landRocker.Query.userVestingTeams(
            first=15_000,
            orderBy=landRocker.UserVestingTeam.startDate,
            orderDirection="desc",
            where=[
                landRocker.UserVestingTeam.hasRevoked == False,
            ]
        )
    
    df = sg.query_df([
        userVestingTeams.vestedAmount,
        userVestingTeams.claimedAmount,
        userVestingTeams.beneficiary.address
    ])        
    
    # Check if the DataFrame is empty
    if df.empty:
        return jsonify({"error": "No records found for the specified collection and token ID"}), 404
    
    total_team_claimed_amount = df['userVestingTeams_claimedAmount'].sum() 
    return total_team_claimed_amount
    # return jsonify({"total_team_claimed_amount": str(total_team_claimed_amount)})

def getStakingCirculation():      
    stakingStat = landRocker.Query.lrtStakingStats()
        
    field_paths = [
        stakingStat.totalClaimedLRTReward
    ]

    df = sg.query_df(field_paths)

    # Check if the DataFrame is empty
    if df.empty:
        return jsonify({"error": "No records found for the specified collection and token ID"})

    # Convert amount and coinAmount to decimal format
    total_stake_circulation = int(df['lrtStakingStats_totalClaimedLRTReward'])

    # total_stake_circulation = df['lrtStakingStats_totalClaimedLRTReward']
    # return total_stake_circulation    
    return total_stake_circulation;
