import json

JSON_FILE = "./hashdroids.json"

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
    # for trait in entry.get("traits"):
    #     if trait.get("c") == "Type":
    #         '''Change None to 1/1'''
    #         type_trait = "1/1" if trait.get("n") == "None" else trait.get("n")

    traits_list.append(
        {
            "hashdroid_id": entry.get("token_id"),
            "traits_count": entry.get("traits_count"),
            "background": entry.get("Background"),
            "eyes": entry.get("Eyes"),
            "hat": entry.get("Hat"),
            "body": entry.get("Body"),
            "ears": entry.get("Ears"),
            "head": entry.get("Head"),
            "mouth": entry.get("Mouth"),
            "top_torso": entry.get("Top Torso"),
            "outfit": entry.get("Outfit"),
            "bottom_torso": entry.get("Bottom Torso"),
            "full_head": entry.get("Full Head"),
            "full_body": entry.get("Full Body"),
            "special": entry.get("Special"),
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
query_prepend = """DROP TABLE IF EXISTS bmc_hashdroids_traits;
CREATE TEMPORARY TABLE bmc_hashdroids_traits AS
SELECT * FROM (VALUES
"""
query_append = """) AS t (hashdroid_id,traits_count,background,eyes,hat,body,ears,head,mouth,top_torso,outfit,bottom_torso,full_head,full_body,special );

SELECT
    *
FROM bmc_hashdroids_traits
ORDER BY hashdroid_id ASC
"""
query_string = str()
for idx, entry in enumerate(traits_list):
    query_val = f"{tuple(entry.values())}"

    if idx == (len(traits_list) - 1):
        query_string += query_val
    else:
        query_string += query_val + "," + "\n"

final_query = query_prepend + query_string + query_append
with open("hashdroids_traits.sql", "w") as f:
    f.write(final_query)
# print(traits_dict)
