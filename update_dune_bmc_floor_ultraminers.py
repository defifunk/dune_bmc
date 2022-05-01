from concurrent.futures import ThreadPoolExecutor 
from web3 import Web3
from decouple import config
import json
import pandas as pd
from get_opensea import get_ultra_miner_floor, get_ultra_price
from dune_local import fetch_records, DuneAPI
from dotenv import load_dotenv
from datetime import datetime

'''web3 components'''
INFURA_URL = "https://mainnet.infura.io/v3"
INFURA_PROJECT = config("INFURA_PROJECT")
w3 = Web3(Web3.HTTPProvider(INFURA_PROJECT))
factory_abi = dict()
with open ("./json/bmcfactoryABI.json", 'r') as f:
    factory_abi = json.load(f)
factory_address = '0x7b32982a32bB71150FCAA99BfBadDD72c1775a10'
factory_contract = w3.eth.contract(address=factory_address, abi=factory_abi, )


# check daily rewards accumulated

def check_ultra_accum_rewards(token_id: int) -> int:
    return factory_contract.functions.checkUltraDailyReward(token_id).call() / 10**18


def check_hash_rewards_mp(token_id_list: list) -> tuple:
    with ThreadPoolExecutor() as executor:
        rewards = executor.map(check_ultra_accum_rewards,token_id_list)
        return rewards

def check_nft_buy_price(token_id_list: list):
    with ThreadPoolExecutor() as executor:
        nft_price = executor.map(get_ultra_price, token_id_list)
        return nft_price

if __name__ == "__main__":
    '''Load from .env for local development'''
    load_dotenv() 
    '''Create a dict'''
    results_list = list()
    '''Get NFT floor ids'''
    
    token_id_list = get_ultra_miner_floor()[0:50] # limit to first 50 results 
    '''Fetch hash rewards based on floor nft ids'''
    mp_results = check_hash_rewards_mp(token_id_list)
    nft_prices = check_nft_buy_price(token_id_list)
    # print(results)
    '''Map 1'''
    for (token_id, rewards, nft_price) in zip(token_id_list, mp_results,nft_prices) :
        results_list.append(
            {
                "ultra_miner_id" : token_id,
                "ETH_buy_price": nft_price,
                "hash_rewards": rewards,
            }
        )
    # print(results_list)
    '''Write to file'''
    df = pd.DataFrame(results_list)
    df.index = df.index + 1
    df_dict = df.to_dict(orient='records')
    print(df_dict)

    '''load from df_dict'''
    json_data = df_dict
    '''Create query string'''
    query_string = str()
    query_prepend = (
"""DROP TABLE IF EXISTS bmc_ultraminer_opensea_floor;
CREATE TEMPORARY TABLE bmc_ultraminer_opensea_floor AS
SELECT * FROM (VALUES
"""
    )
    query_append = (
""") AS t (ultra_miner_id, ETH_buy_price, hash_rewards);

SELECT 
    CONCAT('<a href="https://opensea.io/assets/0x0c6822ca73de6871f27acd9ca05a05b99294b805/', "ultra_miner_id",'" target="_blank">🌊</a> ', "ultra_miner_id") AS ultra_miner,
    ETH_buy_price,
    hash_rewards
FROM bmc_ultraminer_opensea_floor
ORDER BY ETH_buy_price ASC
"""
    )

    for idx, entry in enumerate(json_data):
        query_val = f'{entry.get("ultra_miner_id"),entry.get("ETH_buy_price"),entry.get("hash_rewards")}'
        
        print(f"{idx} - {query_val}")
        if idx == (len(json_data) - 1) :
            query_string += query_val
        else:
            query_string += query_val + ',' + '\n'
    
    final_query = query_prepend + query_string + query_append
    with open('generated_hash_value.sql' ,'w') as f:
        f.write(final_query)

    '''Get time'''
    now = datetime.now().utcnow()
    datetime_val = now.strftime("%Y-%m-%d %H:%M")
    
    '''Rune Dune'''
    dune_connection = DuneAPI.new_from_environment()
    records = fetch_records(
        dune_connection,
        query_name=f"BMC Ultraminers - Opensea Floor",
        query_description=f"Update interval: 15mins (last updated: {datetime_val} UTC)")
    print("First result:", records[0])