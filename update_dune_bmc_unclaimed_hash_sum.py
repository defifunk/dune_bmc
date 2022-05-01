from dune_local import fetch_records, DuneAPI
from dotenv import load_dotenv
from datetime import datetime

if __name__ == "__main__":
    '''Load from .env for local development'''
    load_dotenv() 
    '''Create query string'''
    query_append = (
"""SELECT
    sum(hash_rewards) AS total_unclaimed_hash
FROM bmc_ultraminer_unclaimed_hash;
"""
    )
    
    '''Fetch generated sql file'''
    current_query = str()
    with open('generated_hash_value.sql' ,'r') as f:
        current_query = f.read()
    final_query = current_query + query_append
    '''Get time'''
    now = datetime.now().utcnow()
    datetime_val = now.strftime("%Y-%m-%d %H:%M")
    
    '''Rune Dune'''
    dune_connection = DuneAPI.new_from_environment()
    records = fetch_records(
        dune_connection,
        query_name=f"BMC Ultraminers - Total Unclaimed HASH",
        query_description=f"Update interval: 1h (last updated: {datetime_val} UTC)")
    print("First result:", records[0])