from brownie import (
    accounts,
    network,
    config,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
    interface
)

from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = [ "mainnet-fork" ]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache-local-new"
]
DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed!")

def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id,password="test")
    if (
            network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
            or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {
    "eth_usd_price_feed" : MockV3Aggregator,
    "vrf_coordinator" : VRFCoordinatorMock,
    "link_token" : LinkToken
}

def get_contract(contract_name):
    """
    This function will grab the contract addresses from brownie config if
    defined otherwise it will deploy a mock version of that contract and return
    that mock contract

        Args: contract_name (string)

        :returns
            brownie.netwoork.contract.ProjectContract: The most recently deployed
            contract
    :return:
    """

    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # abi
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
         )

    return contract

def fund_with_link(contract_address, account=None, link_token=None, amount=10 ** 17):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)

    print("Funded contract")
    return tx