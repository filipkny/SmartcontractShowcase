from brownie import SmartcontractShowcase
from scripts.helpful_scripts import get_account
from web3 import Web3

def main():
    account = get_account()
    smartcontract_showcase = SmartcontractShowcase[-1]
    creation_txn = smartcontract_showcase.mint(1,{"from": account, "value": Web3.toWei(0.1, "ether")})
    creation_txn.wait(1)

