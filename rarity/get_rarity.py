import json

JSON_FILE = "./ultraminer_traits.json"

traits_dict = dict()
with open(JSON_FILE, "r") as f:
    traits_dict = json.load(f)


traits_list = list()


"""
Loop over all entries
"""
for entry in traits_dict:
    """Get Ultraminer Type"""
    type_trait = str()
    for trait in entry.get("traits"):
        if trait.get("c") == "Type":
            """Change None to 1/1"""
            type_trait = "1/1" if trait.get("n") == "None" else trait.get("n")

    traits_list.append(
        {
            "ultra_miner_id": entry.get("id"),
            "rairty_id": entry.get("positionId"),
            "type": type_trait,
        }
    )

"""
save traits to file
"""
# OUTPUT_FILE = "./traits_list.json"
# with open (OUTPUT_FILE, 'w') as f:
#     f.write(json.dumps(traits_list))

"""
generate sql statement
"""
query_prepend = """DROP TABLE IF EXISTS bmc_ultraminer_opensea_floor;
CREATE TEMPORARY TABLE bmc_ultraminer_opensea_floor AS
SELECT * FROM (VALUES
"""
query_append = """) AS t (ultra_miner_id, ETH_buy_price, hash_rewards);

SELECT 
    CONCAT('<a href="https://opensea.io/assets/0x0c6822ca73de6871f27acd9ca05a05b99294b805/', "ultra_miner_id",'" target="_blank">🌊</a> ', "ultra_miner_id") AS ultra_miner,
    ETH_buy_price,
    hash_rewards
FROM bmc_ultraminer_opensea_floor
ORDER BY ETH_buy_price ASC
"""
query_string = str()
for idx, entry in enumerate(traits_list):
    query_val = (
        f'{entry.get("ultra_miner_id"),entry.get("rairty_id"),entry.get("type")}'
    )

    if idx == (len(traits_list) - 1):
        query_string += query_val
    else:
        query_string += query_val + "," + "\n"

# final_query = query_prepend + query_string + query_append
with open("ultraminer_traits.sql", "w") as f:
    f.write(query_string)
# print(traits_dict)
