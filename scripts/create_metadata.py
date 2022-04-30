import json

import requests
from brownie import SmartcontractShowcase, network
from pathlib import Path

def main():
    smartcontract_showcase = SmartcontractShowcase[-1]
    num_tokens =  smartcontract_showcase.totalSupply()

    # reading the data from the file
    if Path('./nfts/uploaded_nfts.txt').exists():
        with open('./nfts/uploaded_nfts.txt') as f:
            data = f.read()

        uploaded_nfts = json.loads(data)
        print("Loaded uploaded nfts")
    else:
        print("No uploaded nfts found")
        uploaded_nfts = {}

    print(f"You have {num_tokens} NFTs")

    for token_id in range(num_tokens):

        metadata_filename = f"./nfts/metadata/tombo{token_id}.json"

        if Path(metadata_filename).exists():
            print(f"{metadata_filename} already exists! Skipping")
        else:
            print(f"Creating {metadata_filename}")
            image_filename = f"./nfts/images/{token_id}.png"
            metadata = {
                "name" : "Tombo#{}".format(token_id),
                "description" : "Tombo's Deniiro #{}".format(token_id),
                "image" : upload_to_ipfs(image_filename),
                "attributes" :[]
            }
            with open(metadata_filename,"w") as file:
                json.dump(metadata, file)
            metadata_uri = upload_to_ipfs(metadata_filename)
            uploaded_nfts[token_id] = metadata_uri

    with open("./nfts/uploaded_nfts.txt", "w") as f:
        json.dump(uploaded_nfts, f)

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        img_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url+endpoint,files={"file": img_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        img_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(img_uri)
        return img_uri
