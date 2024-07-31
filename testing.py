from web3 import Web3
import json

# Подключение к Infura
infura_url = 'https://mainnet.infura.io/v3/42cfa11bcf67482694f1c92e11753dc1'
web3 = Web3(Web3.HTTPProvider(infura_url))

# Проверка подключения
if not web3.is_connected():
    raise Exception("Не удалось подключиться к Ethereum")

# Адреса токенов
eth_address = web3.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")  # WETH
usdt_address = web3.to_checksum_address("0xdAC17F958D2ee523a2206206994597C13D831ec7")  # USDT

# Адрес Uniswap V3 Factory контракта
factory_address = web3.to_checksum_address("0x1F98431c8aD98523631AE4a59f267346ea31F984")

# ABI для Uniswap V3 Factory контракта
factory_abi = json.loads('''
[
    {
        "inputs": [
            {"internalType": "address", "name": "tokenA", "type": "address"},
            {"internalType": "address", "name": "tokenB", "type": "address"},
            {"internalType": "uint24", "name": "fee", "type": "uint24"}
        ],
        "name": "getPool",
        "outputs": [{"internalType": "address", "name": "pool", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]
''')

factory_contract = web3.eth.contract(address=factory_address, abi=factory_abi)

# ABI для пула Uniswap V3
pool_abi = json.loads('''
[
    {
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
            {"internalType": "int24", "name": "tick", "type": "int24"},
            {"internalType": "uint16", "name": "observationIndex", "type": "uint16"},
            {"internalType": "uint16", "name": "observationCardinality", "type": "uint16"},
            {"internalType": "uint16", "name": "observationCardinalityNext", "type": "uint16"},
            {"internalType": "uint8", "name": "feeProtocol", "type": "uint8"},
            {"internalType": "bool", "name": "unlocked", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
''')

# Функция для получения пула по токенам и комиссии
def get_pool(tokenA, tokenB, fee):
    return factory_contract.functions.getPool(tokenA, tokenB, fee).call()

# Возможные комиссии в Uniswap V3
fees = [500, 3000, 10000]

# Функция для получения цены из пула
def get_price(pool_address):
    pool_contract = web3.eth.contract(address=pool_address, abi=pool_abi)
    slot0 = pool_contract.functions.slot0().call()
    sqrt_price_x96 = slot0[0]
    price = (sqrt_price_x96 / 2**96) ** 2
    return price

# Функция для расчета стоимости газа
def get_gas_cost():
    gas_price = web3.eth.gas_price
    estimated_gas = 200000  # Примерное количество газа для выполнения свопа
    return gas_price * estimated_gas

# Сканирование всех пулов для заданной пары токенов
pools = []
for fee in fees:
    pool = get_pool(eth_address, usdt_address, fee)
    if pool != '0x0000000000000000000000000000000000000000':
        pools.append((pool, fee))

if len(pools) < 2:
    raise Exception("Недостаточно пулов для сравнения цен")

# Получение цен и расчет арбитражных возможностей
prices = []
for pool, fee in pools:
    price = get_price(pool)
    prices.append((price, pool, fee))

# Сравнение цен и расчет арбитражной возможности
for i in range(len(prices)):
    for j in range(i + 1, len(prices)):
        price1, pool1, fee1 = prices[i]
        price2, pool2, fee2 = prices[j]
        price_difference_percent = abs(price1 - price2) / ((price1 + price2) / 2) * 100

        # Вывод результатов
        print(f'Адрес пула 1: {pool1} с комиссией {fee1}')
        print(f'Цена ETH/USDT в пуле 1: {price1}')
        print(f'Адрес пула 2: {pool2} с комиссией {fee2}')
        print(f'Цена ETH/USDT в пуле 2: {price2}')
        print(f'Разница в цене: {price_difference_percent:.2f}%')

        if price_difference_percent > 0.5:
            gas_cost = get_gas_cost()
            potential_profit = abs(price1 - price2) - gas_cost
            if potential_profit > 0:
                print("Возможна арбитражная возможность с потенциальной прибылью:")
                print(f'Потенциальная прибыль: {potential_profit} ETH (учитывая газ)')
            else:
                print("Возможна арбитражная возможность, но без учета прибыли из-за затрат на газ")
        else:
            print("Арбитражная возможность отсутствует.")
