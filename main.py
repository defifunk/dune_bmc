from duneapi.api import DuneAPI
from duneapi.types import Network, QueryParameter, DuneRecord, DuneQuery
from duneapi.util import open_query
from datetime import datetime
import json


def fetch_records(dune: DuneAPI) -> list[DuneRecord]:
    '''Get time'''
    now = datetime.now()
    datetime_val = now.strftime("%Y-%m-%d %H:%M")
    sample_query = DuneQuery.from_environment(
        raw_sql=open_query("./generated_hash_value.sql"),
        name=f"BMC Ultraminers - Unclaimed HASH (last updated: {datetime_val}",
        network=Network.MAINNET,
        parameters=[
            QueryParameter.number_type("IntParam", 10),
            QueryParameter.date_type("DateParam", datetime(2022, 3, 10, 12, 30, 30)),
            QueryParameter.text_type("TextParam", "aba"),
        ],
    )
    return dune.fetch(sample_query)


if __name__ == "__main__":

    '''Load JSON data'''
    json_data = ""
    with open ("./bmc_hash_rewards.json", 'r') as f:
        json_data = json.load(f)
    print(json_data)
    print(type(json_data))
    '''Create query string'''
    query_string = str()
    query_prepend = (
"""DROP TABLE IF EXISTS my_table;
CREATE TEMPORARY TABLE my_table AS
SELECT * FROM (VALUES
"""
    )
    query_append = (
""") AS t (ultra_miner_id, ETH_buy_price, hash_rewards);
SELECT * FROM my_table;
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

    '''Rune Dune'''
    dune_connection = DuneAPI.new_from_environment()
    records = fetch_records(dune_connection)
    print("First result:", records[0])