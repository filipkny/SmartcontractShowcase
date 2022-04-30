const fs = require('fs');

const Web3 = require('web3');
const web3 = new Web3(Web3.givenProvider);

const addresses = require('./addresses.json');

const signer = web3.eth.accounts.privateKeyToAccount(
    "0x8e3528bc13ea9879359f119e27e6ea62166be5e368e7fb3b878828ce2c8c83aa"
);

const badSigner  = web3.eth.accounts.privateKeyToAccount(
    "0x416b8a7d9290502f5661da81f0cf43893e3d19cb9aea3c426cfb36e8186e9c09"
);

let signedMessages = {};
let badSignedMessages ={};
// Sign messages whitelisted users. These signatures will
// allow these addresses to claim either 3, 2 or 1 tokens
for (let address of addresses) {

    // Construct message to sign.
    let message = `0x000000000000000000000000${address.substring(2)}`;
    console.log(`Signing ${address} :: ${message}`);

    // Sign the message, update the `signedMessages` dict
    // storing only the `signature` value returned from .sign()
    let { signature } = signer.sign(message);

    console.log(`Signature ${signature}`)
    signedMessages[address] = signature;

}

for (let address of addresses) {

    // Construct message to sign.
    let message = `0x000000000000000000000000${address.substring(2)}`;
    console.log(`Signing ${address} :: ${message}`);

    // Sign the message, update the `signedMessages` dict
    // storing only the `signature` value returned from .sign()
    let { signature } = badSigner.sign(message);

    console.log(`Bad signature ${signature}`)
    badSignedMessages[address] = signature;

}


fs.writeFileSync('./signatures_test.json', JSON.stringify(signedMessages, null, 2), 'utf8');
fs.writeFileSync('./bad_signatures_test.json', JSON.stringify(badSignedMessages, null, 2), 'utf8');
console.log("Signatures Written > `./signatures_test.json`");
console.log("Bad signatures Written > `./bad_signatures_test.json`");