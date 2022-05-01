import requests
from requests.exceptions import HTTPError
import re
from bs4 import BeautifulSoup


def get_ultra_miner_floor() -> list:
    url_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    buy_now_url = "https://opensea.io/collection/ultra-miners?search[sortAscending]=true&search[sortBy]=PRICE&search[toggles][0]=BUY_NOW"
    
    try:
        response = requests.get(
        url=buy_now_url,
        headers=url_headers)
    # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    
    html = str(response.content)

    '''
    Use regex to match ULTRA MINER #XXXX
    '''
    regex = r"ULTRA MINER \#[0-9]{2,5}"
    pattern = re.compile(regex)
    matches_list = re.findall(pattern, html)
    # print(f"matches_list: {matches_list}")
    '''
    Strip "ULTRA MINER #XXXX" to Int
    '''
    nft_token_id = list()
    for id in matches_list:
        int_val = int(id.strip("ULTRA MINER #"))
        nft_token_id.append(int_val)
    # print(f"nft_token_id:{nft_token_id}")
    '''Remove duplicates'''
    nft_token_id = list(set(nft_token_id))
    return nft_token_id

def get_ultra_price(miner_nft_id: str) -> str:
    BASE_URL = "https://opensea.io/assets"
    NFT_CONTRACT_ADDR = "0x0c6822ca73de6871f27acd9ca05a05b99294b805"

    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    REQ_URL = BASE_URL + "/" + NFT_CONTRACT_ADDR + "/" + str(miner_nft_id)
    
    try:
        response = requests.get(REQ_URL, headers=custom_headers)
    # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    soup = BeautifulSoup(response.text, 'html.parser')
    soup_val = soup.find(class_="Price--amount")

    return soup_val.get_text().strip() if soup_val else ''
