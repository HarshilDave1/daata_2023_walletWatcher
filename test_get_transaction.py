import requests

chain_id = 1 # for mainnet
safe = '0x171a3ad89cFb7888342f10F4740F72e6F6098A4C'
url = f'https://api.covalenthq.com/v1/eth-mainnet/address/{safe}/transactions_v3/?key={API_KEY}&with-safe=true&no-logs=true'
r = requests.get(url)
data = r.json()

data
## Example output:
# {'data': {'address': '0x171a3ad89cfb7888342f10f4740f72e6f6098a4c',
#   'updated_at': '2023-10-14T16:28:55.358138539Z',
#   'next_update_at': '2023-10-14T16:33:55.358139022Z',
#   'quote_currency': 'USD',
#   'chain_id': 1,
#   'chain_name': 'eth-mainnet',
#   'current_page': 0,
#   'links': {'prev': None, 'next': None},
#   'items': [{'block_signed_at': '2023-09-17T04:12:11Z',
#     'block_height': 18153327,
#     'block_hash': '0x9bc3e79280aca97eb954a4f8ca9d2189d62f18d2eef0e524fa3e5dff2ee8c465',
#     'tx_hash': '0x8c2df626221acfd2f3a294e2836933ae8ea125b6ac751e75e6edca8944a61780',
#     'tx_offset': 109,
#     'successful': True,
#     'miner_address': '0x1f9090aae28b8a3dceadf281b0f12828e676c326',
#     'from_address': '0x6e19fc0ce57081420ca1f60f5ebe46b2c55cc5e0',
#     'from_address_label': None,
#     'to_address': '0xa6b71e26c5e0845f74c812102ca7114b6a896ab2',
#     'to_address_label': None,
#     'value': '0',
#     'value_quote': 0.0,
#     'pretty_value_quote': '$0.00',
#     'gas_metadata': {'contract_decimals': 18,
#      'contract_name': 'Ether',
#      'contract_ticker_symbol': 'ETH',
#      'contract_address': '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
#      'supports_erc': None,
#      'logo_url': 'https://www.datocms-assets.com/86369/1669653891-eth.svg'},
#     'gas_offered': 261619,
#     'gas_spent': 258640,
#     'gas_price': 8000000000,
#     'fees_paid': '2069120000000000',
#     'gas_quote': 3.3598412347613213,
#     'pretty_gas_quote': '$3.36',
#     'gas_quote_rate': 1623.8020195838433}]},
#  'error': False,
#  'error_message': None,
#  'error_code': None}
