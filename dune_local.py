from duneapi.api import DuneAPI
from duneapi.types import Network, QueryParameter, DuneRecord, DuneQuery
from duneapi.util import open_query
from datetime import datetime


def fetch_records(dune: DuneAPI) -> list[DuneRecord]:
    '''Get time'''
    now = datetime.now().utcnow()
    datetime_val = now.strftime("%Y-%m-%d %H:%M")
    sample_query = DuneQuery.from_environment(
        raw_sql=open_query("./generated_hash_value.sql"),
        name=f"BMC Ultraminers - Unclaimed HASH (last updated: {datetime_val} UTC)",
        description=f"Update interval: 30minutes",
        network=Network.MAINNET,
        parameters=[
            # QueryParameter.number_type("IntParam", 10),
            # QueryParameter.date_type("DateParam", datetime(2022, 3, 10, 12, 30, 30)),
            # QueryParameter.text_type("TextParam", "aba"),
        ],
    )
    return dune.fetch(sample_query)
