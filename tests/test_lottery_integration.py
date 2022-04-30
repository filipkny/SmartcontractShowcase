import pytest
from brownie import network, accounts
from web3 import Web3

from scripts.deploy_smartcontract import deploy_smartcontract_showcase
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account


def test_mint_integration():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipSaleState(
        {"from": owner_account}
    )

    smartcontract_showcase.mint(1, {"from": accounts[0], "value": Web3.toWei(0.1, "ether")})

    assert smartcontract_showcase.balanceOf(accounts[0]) == 1
