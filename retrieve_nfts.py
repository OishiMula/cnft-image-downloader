import os, requests, json, ipfsApi
from dotenv import load_dotenv
load_dotenv()

blockfrost_api = {"project_id" : os.getenv("BLOCKFROST_TOKEN")}
blockfrost_address_base = 'https://cardano-mainnet.blockfrost.io/api/v0/addresses/'
blockfrost_asset_base = 'https://cardano-mainnet.blockfrost.io/api/v0/assets/'
blockfrost_stake_base = 'https://cardano-mainnet.blockfrost.io/api/v0/accounts/'
ipfs_base ='https://infura-ipfs.io/ipfs/'
complete_flag = 0

# Retrieve the address, start the function
while complete_flag == 0:
    address = input(("Cardano NFT Image Retrieval\n"
        "Created by Oishi Mula, 3/6/22\n"
        "Please enter an address.\n>>>"))
    file_path = input("Please enter a location to download the images\n>>>")
    response_API = requests.get(blockfrost_address_base + address, headers=blockfrost_api)
    blockfrost_address_data = response_API.json()
    stake_address = blockfrost_address_data['stake_address']
    resposne_API2 = requests.get(blockfrost_stake_base + stake_address + '/addresses/assets', headers=blockfrost_api)
    blockfrost_stake_data = resposne_API2.json()
    
    multiple_pages = 1
    page = 1
    while multiple_pages == 1:
        print(f"{len(blockfrost_stake_data)} NFTs were found. Starting the download.")
        if len(blockfrost_stake_data) == 100:
            page += 1
        else:
            multiple_pages = 0
            
        for asset in blockfrost_stake_data:
            if asset == 'lovelace':
                continue
            response_API3 = requests.get(blockfrost_asset_base + str(asset['unit']), headers=blockfrost_api)
            blockfrost_asset_data = response_API3.json()
            try:
                asset_img_ipfs = blockfrost_asset_data['onchain_metadata']['image'][7:]
                name = blockfrost_asset_data['onchain_metadata']['name']
                name = name.replace('-', '')
                name = name.replace('.', '')
                name = name.replace('|', '')
                name = name.replace('[', '')
                name = name.replace(']', '')
                name = name.replace(':', '')
                img_data = requests.get(ipfs_base + asset_img_ipfs) 
                filetype = None
                match img_data.headers['Content-Type']:
                    case 'image/png':
                        filetype = '.png'
                    case 'image/jpeg':
                        filetype = '.jpeg'
                    case 'image/gif':
                        filetype = '.gif'
                    case 'video/mp4':
                        filetype = '.mp4'
                fullpath = file_path + name + filetype
                if os.path.isfile(fullpath):
                    print(f"Skipping {name}")
                    continue
                with open(os.path.join(file_path, name + filetype), 'wb') as image:
                    print(f"Processing {name}")
                    image.write(img_data.content)
            except:
                continue
        resposne_API_multipage = requests.get(blockfrost_stake_base + stake_address + '/addresses/assets?page=' + str(page), headers=blockfrost_api)
        blockfrost_stake_data = resposne_API_multipage.json()
    
    end_prompt = 0
    while end_prompt == 0: 
        print("NFT Image Retrieval completed.")
        response = input(("Would you like to retrieve NFT images from another address?\n"
            "(Y) - Yes\n"
            "(Q) - Quit the Program\n>>>"))
      
        match response.lower():
            case 'y':
                end_prompt = 1
                continue
            case 'q':
                end_prompt = 1
                complete_flag = 1
            case _:
                print("Retry that option again.")
                
print("Thanks for using Cardano NFT Image Retrieval!")
quit()
    
