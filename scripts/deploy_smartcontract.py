from brownie import config, network, SmartcontractShowcase

from scripts.helpful_scripts import get_account, get_contract, fund_with_link
import time

def main():
    deploy_smartcontract_showcase()

def deploy_smartcontract_showcase():
    account = get_account()
    print(f"Owner account {account}")
    lottery =  SmartcontractShowcase.deploy(
        "SmartcontractShowcase",
        "SS",
        1646755882,
        {"from" : account},
        publish_source=False
    )

    print("Deployed lottery")
    return lottery
