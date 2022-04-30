import brownie
import pytest
from brownie import network, accounts
from web3 import Web3
import json
import js2py

from scripts.deploy_smartcontract import deploy_smartcontract_showcase
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from web3.auto import w3
from eth_account.messages import encode_defunct


def test_deploy_smartcontract():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    smartcontract_showcase = deploy_smartcontract_showcase()

    assert True

def test_mint_allow_list():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipIsAllowListActive(
        {"from": owner_account}
    )
    smartcontract_showcase.setAllowList(
        [accounts[0],
         accounts[1]],
        1,
        {"from":owner_account}
    )

    smartcontract_showcase.mintAllowList(1, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

    assert smartcontract_showcase.balanceOf(accounts[0]) == 1

def test_fail_mint_allow_list_not_enough_eth():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipIsAllowListActive(
        {"from": owner_account}
    )
    smartcontract_showcase.setAllowList(
        [accounts[0],
         accounts[1]],
        1,
        {"from":owner_account}
    )

    with brownie.reverts("Not enough ETH to mint the provided number of tokens"):
        smartcontract_showcase.mintAllowList(1, {"from": accounts[0], "value": Web3.toWei(0.01, "ether")})

def test_fail_mint_allow_list_not_in_allow_list():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipIsAllowListActive(
        {"from": owner_account}
    )
    smartcontract_showcase.setAllowList(
        [accounts[0],
         accounts[1]],
        1,
        {"from":owner_account}
    )

    with brownie.reverts("Exceeded max limit of allowed token mints"):
        smartcontract_showcase.mintAllowList(1, {"from": accounts[2], "value": Web3.toWei(1, "ether")})

def test_fail_mint_allow_list_not_active():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract_showcase = deploy_smartcontract_showcase()

    smartcontract_showcase.setAllowList(
        [accounts[0],
         accounts[1]],
        1,
        {"from":owner_account}
    )

    with brownie.reverts("Allow list is not active"):
        smartcontract_showcase.mintAllowList(1, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

def test_fail_mint_allow_list_exceeded_number():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipIsAllowListActive({"from":owner_account})

    toMint = 255

    smartcontract_showcase.setAllowList(
        [acc.address for acc in accounts],
        toMint,
        {"from":owner_account}
    )

    with brownie.reverts("Exceeded max supply"):
        for acc in accounts:
            smartcontract_showcase.mintAllowList(toMint, {"from": acc, "value": Web3.toWei(22, "ether")})

def test_fail_mint_allow_list_after_minting_already():

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipIsAllowListActive(
        {"from": owner_account}
    )
    smartcontract_showcase.setAllowList(
        [accounts[0],
         accounts[1]],
        1,
        {"from":owner_account}
    )

    with brownie.reverts("Exceeded max limit of allowed token mints"):
        smartcontract_showcase.mintAllowList(1, {"from": accounts[2], "value": Web3.toWei(1, "ether")})
        smartcontract_showcase.mintAllowList(1, {"from": accounts[2], "value": Web3.toWei(1, "ether")})

def test_mint():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipSaleState(
        {"from": owner_account}
    )

    smartcontract_showcase.mint(1, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

    assert smartcontract_showcase.balanceOf(accounts[0]) == 1
    assert smartcontract_showcase.totalSupply() == 1

def test_mint_several():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipSaleState(
        {"from": owner_account}
    )

    smartcontract_showcase.mint(5, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

    assert smartcontract_showcase.balanceOf(accounts[0]) == 5
    assert smartcontract_showcase.totalSupply() == 5

def test_fail_mint_sale_not_active():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract_showcase = deploy_smartcontract_showcase()


    with brownie.reverts("Sale is not active"):
        smartcontract_showcase.mint(1, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

def test_fail_mint_sale_exceeded_max_amount_mints():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract_showcase = deploy_smartcontract_showcase()


    with brownie.reverts("Sale is not active"):
        smartcontract_showcase.mint(1, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

def test_fail_mint_not_enough_eth():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipSaleState()

    with brownie.reverts("Not enough ETH to mint the provided number of tokens"):
        smartcontract_showcase.mint(1, {"from": accounts[0], "value": Web3.toWei(0.07, "ether")})

def test_fail_mint_exceeded_max_supply():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipSaleState()



    with brownie.reverts("Exceeded max limit of allowed token mints"):
        for _ in range(100):
            smartcontract_showcase.mint(100, {"from": accounts[0], "value": Web3.toWei(8, "ether")})

        smartcontract_showcase.mint(1, {"from": accounts[0], "value": Web3.toWei(8, "ether")})

def test_whitdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    og_owner_amount = owner_account.balance()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipSaleState({"from": owner_account})

    smartcontract_showcase.mint(1, {"from": accounts[1], "value": Web3.toWei(8, "ether")})
    smartcontract_showcase.withdraw({"from":owner_account})

    assert owner_account.balance() > og_owner_amount

def test_balance_of():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    og_owner_amount = owner_account.balance()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipSaleState({"from": owner_account})

    smartcontract_showcase.mint(1, {"from": accounts[1], "value": Web3.toWei(8, "ether")})

    assert smartcontract_showcase.balanceOf(accounts[1]) == 1

def test_emergency_start_index_block():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    og_owner_amount = owner_account.balance()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.emergencySetStartingIndexBlock()

    assert smartcontract_showcase.startingIndex() == 0

def test_fail_emergency_start_index_already_set():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    og_owner_amount = owner_account.balance()
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.emergencySetStartingIndexBlock()
    smartcontract_showcase.setStartingIndex()

    with brownie.reverts("Starting index is already set"):
        smartcontract_showcase.emergencySetStartingIndexBlock()

def test_set_starting_index():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()

    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.emergencySetStartingIndexBlock()
    smartcontract_showcase.setStartingIndex()

    assert smartcontract_showcase.startingIndex() > 0

def test_fail_emergency_start_index_block_not_set():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    og_owner_amount = owner_account.balance()
    smartcontract_showcase = deploy_smartcontract_showcase()

    with brownie.reverts("Starting index block must be set"):
        smartcontract_showcase.setStartingIndex()

def test_signing():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()


    # Load accounts
    owner_account = get_account()
    signing_account = get_account(id="signing-account")

    # Load signatures
    signatures = load_signatures_json("signatures_test")


    # Deploy contract and set sale to active
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipSaleState(
        {"from": owner_account}
    )

    # Mint
    signature = signatures[accounts[0].address]
    smartcontract_showcase.mint(1, signature, {"from": accounts[0], "value": Web3.toWei(1, "ether")})

    assert smartcontract_showcase.balanceOf(accounts[0]) == 1

def test_signing_signer_mismatch():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()


    # Load accounts
    owner_account = get_account()
    random = get_account(id="random")
    print(f"Random address {random.address}")

    # Load signatures
    signatures = load_signatures_json("signatures_test")
    bad_signatures = load_signatures_json("bad_signatures_test")

    # Deploy contract and set sale to active
    smartcontract_showcase = deploy_smartcontract_showcase()
    smartcontract_showcase.flipSaleState(
        {"from": owner_account}
    )

    # Mint
    print(bad_signatures[random.address])
    with brownie.reverts("Signer address mismatch."):
        smartcontract_showcase.mint(1, bad_signatures[random.address], {"from": accounts[0], "value": Web3.toWei(1, "ether")})



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