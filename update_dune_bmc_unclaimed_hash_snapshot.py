from concurrent.futures import ThreadPoolExecutor
from web3 import Web3
from decouple import config
import json
import pandas as pd
from get_opensea import get_ultra_miner_floor, get_ultra_price
from dune_local import fetch_records, DuneAPI
from dotenv import load_dotenv
from datetime import datetime

"""web3 components"""
INFURA_URL = "https://mainnet.infura.io/v3"
factory_address = "0x7b32982a32bB71150FCAA99BfBadDD72c1775a10"
factory_abi = dict()
with open("./json/bmcfactoryABI.json", "r") as f:
    factory_abi = json.load(f)
"""INFURA Endpoint #1"""
INFURA_PROJECT_1 = config("INFURA_PROJECT_1")
w3_1 = Web3(Web3.HTTPProvider(INFURA_PROJECT_1))
factory_contract_1 = w3_1.eth.contract(
    address=factory_address,
    abi=factory_abi,
)
"""INFURA Endpoint #2"""
INFURA_PROJECT_2 = config("INFURA_PROJECT_2")
w3_2 = Web3(Web3.HTTPProvider(INFURA_PROJECT_2))
factory_contract_2 = w3_2.eth.contract(
    address=factory_address,
    abi=factory_abi,
)
"""INFURA Endpoint #3"""
INFURA_PROJECT_3 = config("INFURA_PROJECT_3")
w3_3 = Web3(Web3.HTTPProvider(INFURA_PROJECT_3))
factory_contract_3 = w3_3.eth.contract(
    address=factory_address,
    abi=factory_abi,
)


# check daily rewards accumulated


def check_ultra_accum_rewards(token_id: int) -> int:
    accum_rewards = ""
    if not accum_rewards:
        try:
            accum_rewards = (
                factory_contract_1.functions.checkUltraDailyReward(token_id).call()
                / 10**18
            )
            print(f"web3_1 went okay")

        except Exception as e:
            print(f"web3_1 exception:{e}")
    if not accum_rewards:
        try:
            accum_rewards = (
                factory_contract_2.functions.checkUltraDailyReward(token_id).call()
                / 10**18
            )
            print(f"web3_2 went okay")

        except Exception as e:
            print(f"web3_2 exception:{e}")
    if not accum_rewards:
        try:
            accum_rewards = (
                factory_contract_3.functions.checkUltraDailyReward(token_id).call()
                / 10**18
            )
            print(f"web3_3 went okay")

        except Exception as e:
            print(f"web3_3 exception:{e}")
            print(f"all endpoints are failed. Exiting loop")
    return accum_rewards if accum_rewards >= 0 else -1


def check_hash_rewards_mp(token_id_list: list) -> tuple:
    with ThreadPoolExecutor() as executor:
        rewards = executor.map(check_ultra_accum_rewards, token_id_list)
        return rewards


def check_nft_buy_price(token_id_list: list):
    with ThreadPoolExecutor() as executor:
        nft_price = executor.map(get_ultra_price, token_id_list)
        return nft_price


if __name__ == "__main__":
    """Load from .env for local development"""
    load_dotenv()
    """Create a dict"""
    results_list = list()
    """Get NFT floor ids"""
    # for all nfts - max 4445
    token_id_list = [i for i in range(0, 4445)]
    """Fetch hash rewards based on floor nft ids"""
    mp_results = check_hash_rewards_mp(token_id_list)
    """Map 2"""
    for (token_id, rewards) in zip(token_id_list, mp_results):
        results_list.append(
            {
                "ultra_miner_id": token_id,
                "hash_rewards": rewards,
            }
        )
    # print(results_list)
    """Write to file"""
    df = pd.DataFrame(results_list)
    df.index = df.index + 1

    """Test saving value as dict"""
    df_dict = df.to_dict(orient="records")
    print(df_dict)
    """load from df_dict"""
    json_data = df_dict
    """Create query string"""
    query_string = str()
    query_prepend = """DROP VIEW IF EXISTS dune_user_generated.defifunk_bmc_ultraminer_unclaimed_hash_snapshot;
CREATE OR REPLACE view dune_user_generated.defifunk_bmc_ultraminer_unclaimed_hash_snapshot
AS
SELECT * FROM (VALUES
"""

    query_append = """) AS t (ultra_miner_id, hash_rewards);
SELECT
    *
FROM dune_user_generated.defifunk_bmc_ultraminer_unclaimed_hash_snapshot
ORDER BY ultra_miner_id ASC
"""

    for idx, entry in enumerate(json_data):
        # query_val = f'{entry.get("ultra_miner_id"),entry.get("ETH_buy_price"),entry.get("hash_rewards")}'
        query_val = f'{entry.get("ultra_miner_id"),entry.get("hash_rewards")}'

        print(f"{idx} - {query_val}")
        if idx == (len(json_data) - 1):
            query_string += query_val
        else:
            query_string += query_val + "," + "\n"

    final_query = query_prepend + query_string + query_append
    with open("generated_hash_value.sql", "w") as f:
        f.write(final_query)

    """Get time"""
    now = datetime.now().utcnow()
    datetime_val = now.strftime("%Y-%m-%d %H:%M")

    """Rune Dune"""
    dune_connection = DuneAPI.new_from_environment()
    records = fetch_records(
        dune_connection,
        query_name=f"BMC Ultraminers - Unclaimed HASH Snapshot View",
        query_description=f"last updated: {datetime_val} UTC",
    )
    print("First result:", records[0])
