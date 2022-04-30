from duneapi.api import DuneAPI
from duneapi.types import Network, QueryParameter, DuneRecord, DuneQuery
from duneapi.util import open_query

def fetch_records(dune: DuneAPI) -> list[DuneRecord]:
    sample_query = DuneQuery.from_environment(
        raw_sql=open_query("PATH_TO_SOME_SQL_FILE"),
        name="Sample Query",
        network=Network.MAINNET,
        parameters=[
            QueryParameter.number_type("IntParam", 10),
            QueryParameter.text_type("TextParam", "aba"),
        ],
    )
    return dune.fetch(sample_query)


if __name__ == "__main__":
    dune_connection = DuneAPI.new_from_environment()
    records = fetch_records(dune_connection)
    print("First result:", records[0])