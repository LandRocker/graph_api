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

    return jsonify(int(Web3.from_wei(total_supply, 'ether')))
       
def getLRTCirculationAmount(): 


    total_supply = 10000000000000000000000000000

    lrt_contract_balance = getUserBalance("0xfb7f8A2C0526D01BFB00192781B7a7761841B16C")
    liquidity = getUserBalance("0x9A0e8cB86CeA03Cd3124b9002884e2d4C806A233")
    game_incentives = getUserBalance("0x1f34744f5ACa6DCA7D6ae27D73367b842bDaF80c")
    marketing = getUserBalance("0xf088d55055aE1A6ad45D3Cf97F7B4c4f7b46Bd79")
    treasury = getUserBalance("0x453b8AD0aae7AD825c6f6C6A257660F5b3fd3f5F")
    team = getUserBalance("0x60E1c0A693C7ac771f12b3fBA694d5D53216E4b1")
    marketing_op1 = getUserBalance("0x5fB4955A9E5C9048e6096292ccE324B9f520184C")
    advisor = getUserBalance("0x27d3Cd95b93101771826A2e0a7564A2dc34aEC3d")
    marketing_op2 = getUserBalance("0x2C8516Dc7F27DC8509Ee9027b28C71C74032ABFd")
    marketing_op3 = getUserBalance("0x4AD2a74568E51f81911a522587A1EFDc821968AE")
    private_sale = getUserBalance("0x71aceEcf818Ab295416e8E59704Af2C894beB174")
    liquidity_provisioning= getUserBalance("0xf3ECa2D9C3C9c6b7BE4B4dA35722Af0DdC7dAA90")
    reserved_wallet = int(lrt_contract_balance) + int(liquidity) + int(game_incentives) + int(marketing) +int(treasury) +int(team) +int(marketing_op1) +int(advisor) +int(marketing_op2) +int(marketing_op3) +int(private_sale) +int(liquidity_provisioning)    # sale_first = getClaimedTokenByPlanId("0x0")      
    
    total_circulation_amount = int(total_supply) - reserved_wallet
   
    total_circulation_amount = Web3.from_wei(total_circulation_amount, 'ether')

    return jsonify(total_circulation_amount)
   
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


def getUserBalance(balance):      
    users = landRocker.Query.users(
        where=[
            landRocker.User.address == balance
        ]
    )
        
    field_paths = [
        users.balance
    ]

    df = sg.query_df(field_paths)

    # Check if the DataFrame is empty
    if df.empty:
        return jsonify({"error": "No records found for the specified collection and token ID"})

    userBalance = df['users_balance']
    return userBalance;
