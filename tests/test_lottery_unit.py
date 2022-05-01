import json

import brownie
import pytest
from brownie import network, accounts
from web3 import Web3

from scripts.deploy_smartcontract import deploy_smartcontract_showcase
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

@pytest.fixture
def smartcontract():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    return deploy_smartcontract_showcase()

def test_deploy_smartcontract(smartcontract):
    assert smartcontract.balanceOf(accounts[0]) == 0

def test_mint_allow_list(smartcontract):

    owner_account = get_account()
    smartcontract.flipIsAllowListActive(
        {"from": owner_account}
    )
    smartcontract.setAllowList(
        [accounts[0],
         accounts[1]],
        1,
        {"from":owner_account}
    )

    smartcontract.mintAllowList(1, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

    assert smartcontract.balanceOf(accounts[0]) == 1

def test_fail_mint_allow_list_not_enough_eth(smartcontract):

    owner_account = get_account()
    smartcontract.flipIsAllowListActive(
        {"from": owner_account}
    )
    smartcontract.setAllowList(
        [accounts[0],
         accounts[1]],
        1,
        {"from":owner_account}
    )

    with brownie.reverts("Not enough ETH to mint the provided number of tokens"):
        smartcontract.mintAllowList(1, {"from": accounts[0], "value": Web3.toWei(0.01, "ether")})

def test_fail_mint_allow_list_not_in_allow_list(smartcontract):

    owner_account = get_account()
    smartcontract.flipIsAllowListActive(
        {"from": owner_account}
    )
    smartcontract.setAllowList(
        [accounts[0],
         accounts[1]],
        1,
        {"from":owner_account}
    )

    with brownie.reverts("Exceeded max limit of allowed token mints"):
        smartcontract.mintAllowList(1, {"from": accounts[2], "value": Web3.toWei(1, "ether")})

def test_fail_mint_allow_list_not_active(smartcontract):
    owner_account = get_account()
    smartcontract.setAllowList(
        [accounts[0],
         accounts[1]],
        1,
        {"from":owner_account}
    )

    with brownie.reverts("Allow list is not active"):
        smartcontract.mintAllowList(1, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

def test_fail_mint_allow_list_exceeded_number(smartcontract):
    owner_account = get_account()
    smartcontract.flipIsAllowListActive({"from":owner_account})

    toMint = 255

    smartcontract.setAllowList(
        [acc.address for acc in accounts],
        toMint,
        {"from":owner_account}
    )

    with brownie.reverts("Exceeded max supply"):
        for acc in accounts:
            smartcontract.mintAllowList(toMint, {"from": acc, "value": Web3.toWei(22, "ether")})

def test_fail_mint_allow_list_after_minting_already(smartcontract):

    owner_account = get_account()
    smartcontract.flipIsAllowListActive(
        {"from": owner_account}
    )
    smartcontract.setAllowList(
        [accounts[0],
         accounts[1]],
        1,
        {"from":owner_account}
    )

    with brownie.reverts("Exceeded max limit of allowed token mints"):
        smartcontract.mintAllowList(1, {"from": accounts[2], "value": Web3.toWei(1, "ether")})
        smartcontract.mintAllowList(1, {"from": accounts[2], "value": Web3.toWei(1, "ether")})

def test_mint(smartcontract):
    owner_account = get_account()

    smartcontract.flipSaleState(
        {"from": owner_account}
    )

    smartcontract.mint(1, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

    assert smartcontract.balanceOf(accounts[0]) == 1
    assert smartcontract.totalSupply() == 1

def test_mint_several(smartcontract):
    owner_account = get_account()
    smartcontract.flipSaleState(
        {"from": owner_account}
    )

    smartcontract.mint(5, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

    assert smartcontract.balanceOf(accounts[0]) == 5
    assert smartcontract.totalSupply() == 5

def test_fail_mint_sale_not_active(smartcontract):
    with brownie.reverts("Sale is not active"):
        smartcontract.mint(1, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

def test_fail_mint_sale_exceeded_max_amount_mints(smartcontract):
    owner_account = get_account()

    with brownie.reverts("Sale is not active"):
        smartcontract.mint(1, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

def test_fail_mint_not_enough_eth(smartcontract):
    smartcontract.flipSaleState()

    with brownie.reverts("Not enough ETH to mint the provided number of tokens"):
        smartcontract.mint(1, {"from": accounts[0], "value": Web3.toWei(0.07, "ether")})

def test_fail_mint_exceeded_max_supply(smartcontract):
    smartcontract.flipSaleState()



    with brownie.reverts("Exceeded max limit of allowed token mints"):
        for _ in range(100):
            smartcontract.mint(100, {"from": accounts[0], "value": Web3.toWei(8, "ether")})

        smartcontract.mint(1, {"from": accounts[0], "value": Web3.toWei(8, "ether")})

def test_whitdraw(smartcontract):

    owner_account = get_account()
    og_owner_amount = owner_account.balance()

    smartcontract.flipSaleState({"from": owner_account})
    smartcontract.mint(1, {"from": accounts[1], "value": Web3.toWei(8, "ether")})
    smartcontract.withdraw({"from":owner_account})

    assert owner_account.balance() > og_owner_amount

def test_balance_of(smartcontract):

    owner_account = get_account()
    og_owner_amount = owner_account.balance()
    smartcontract.flipSaleState({"from": owner_account})

    smartcontract.mint(1, {"from": accounts[1], "value": Web3.toWei(8, "ether")})

    assert smartcontract.balanceOf(accounts[1]) == 1

def test_emergency_start_index_block(smartcontract):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract.emergencySetStartingIndexBlock()

    assert smartcontract.startingIndex() == 0

def test_fail_emergency_start_index_already_set(smartcontract):
    owner_account = get_account()
    smartcontract.emergencySetStartingIndexBlock()
    smartcontract.setStartingIndex()

    with brownie.reverts("Starting index is already set"):
        smartcontract.emergencySetStartingIndexBlock()

def test_set_starting_index(smartcontract):
    smartcontract.emergencySetStartingIndexBlock()
    smartcontract.setStartingIndex()

    assert smartcontract.startingIndex() > 0

def test_fail_emergency_start_index_block_not_set(smartcontract):
    with brownie.reverts("Starting index block must be set"):
        smartcontract.setStartingIndex()

def test_signing(smartcontract):

    # Load accounts
    owner_account = get_account()
    signatures = load_signatures_json("signatures_test")


    # Deploy contract and set sale to active
    smartcontract.flipSaleState(
        {"from": owner_account}
    )

    # Mint
    signature = signatures[accounts[0].address]
    smartcontract.mint(1, signature, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

    assert smartcontract.balanceOf(accounts[0]) == 1

def test_signing_signer_mismatch(smartcontract):
    # Load accounts
    owner_account = get_account()
    random = get_account(id="random")
    print(f"Random address {random.address}")

    # Load signatures
    signatures = load_signatures_json("signatures_test")
    bad_signatures = load_signatures_json("bad_signatures_test")

    # Deploy contract and set sale to active
    smartcontract.flipSaleState(
        {"from": owner_account}
    )

    # Mint
    print(bad_signatures[random.address])
    with brownie.reverts("Signer address mismatch."):
        smartcontract.mint(1, bad_signatures[random.address], {"from": accounts[0], "value": Web3.toWei(1, "ether")})


def generate_signatures_json(accounts, signing_account):

    signed_messages = {}

    print(f"Signing address {signing_account.address}")
    print(f"Signing private key {signing_account.private_key}")

    for acc in accounts[:1]:
        m = "0x000000000000000000000000" + acc.address[2:]
        message = m
        print(f"Signing {acc.address} :: {message}")
        signed_message = signing_account.sign_defunct_message(message)
        print(f"Signed message, type {type(signed_message.signature)}, value: {signed_message.signature.hex()}")
        signed_messages[acc.address] = signed_message

    print("Signed messages")
    return signed_messages

def load_signatures_json(f):
    with open(f"../tests/signing/{f}.json",'r') as f:
        return json.loads(f.read())