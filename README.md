# Workflow #1
DUNE_QUERY_ID=655247
1. Checks unclaimed hash for 1-4445
2. creates a dict of
```json
{
    "ultra_miner_id" : token_id,
    "hash_rewards": rewards,
}
```
3. Generates sql query
4. Submits SQL query to DUNE_QUERY_ID