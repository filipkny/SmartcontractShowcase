

import requests
from brownie import SmartcontractShowcase, network
from pathlib import Path

from scripts.helpful_scripts import get_account

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

def main():
    smartcontract_showcase = SmartcontractShowcase[-1]
    num_tokens =  smartcontract_showcase.totalSupply()

    print(f"You have {num_tokens} NFTs")

    for token_id in range(num_tokens):
        if not smartcontract_showcase.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            metadata_filename = f"./nfts/metadata/tombo{token_id}.json"
            set_tokenURI(token_id, smartcontract_showcase,metadata_filename)


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract._setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_FORMAT.format(nft_contract.address, token_id)}"
    )