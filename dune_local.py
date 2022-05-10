from duneapi.api import DuneAPI
from duneapi.types import Network, QueryParameter, DuneRecord, DuneQuery
from duneapi.util import open_query



def fetch_records(dune: DuneAPI,query_name:str, query_description: str) -> list[DuneRecord]:
    sample_query = DuneQuery.from_environment(
        raw_sql=open_query("./generated_hash_value.sql"),
        name=query_name,
        description=query_description,
        network=Network.MAINNET,
        parameters=[
            # QueryParameter.number_type("IntParam", 10),
            # QueryParameter.date_type("DateParam", datetime(2022, 3, 10, 12, 30, 30)),
            # QueryParameter.text_type("TextParam", "aba"),
        ],
    )
    return dune.fetch(sample_query)
