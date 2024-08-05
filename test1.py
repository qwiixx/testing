import json
import time
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import TransactionNotFound, TimeExhausted
import random

# Константы
INFURA_URL = "https://mainnet.infura.io/v3/42cfa11bcf67482694f1c92e11753dc1"

# Инициализация web3
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Загрузка ABI смарт-контрактов
woo_router_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_weth","type":"address"},{"internalType":"address","name":"_pool","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newPool","type":"address"}],"name":"WooPoolChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"enum IWooRouterV2.SwapType","name":"swapType","type":"uint8"},{"indexed":true,"internalType":"address","name":"fromToken","type":"address"},{"indexed":true,"internalType":"address","name":"toToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"fromAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"toAmount","type":"uint256"},{"indexed":false,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"address","name":"rebateTo","type":"address"}],"name":"WooRouterSwap","type":"event"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"approveTarget","type":"address"},{"internalType":"address","name":"swapTarget","type":"address"},{"internalType":"address","name":"fromToken","type":"address"},{"internalType":"address","name":"toToken","type":"address"},{"internalType":"uint256","name":"fromAmount","type":"uint256"},{"internalType":"uint256","name":"minToAmount","type":"uint256"},{"internalType":"address payable","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"externalSwap","outputs":[{"internalType":"uint256","name":"realToAmount","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"stuckToken","type":"address"}],"name":"inCaseTokenGotStuck","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"stuckTokens","type":"address[]"}],"name":"inCaseTokensGotStuck","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isWhitelisted","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"fromToken","type":"address"},{"internalType":"address","name":"toToken","type":"address"},{"internalType":"uint256","name":"fromAmount","type":"uint256"}],"name":"querySwap","outputs":[{"internalType":"uint256","name":"toAmount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"quoteToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newPool","type":"address"}],"name":"setPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"bool","name":"whitelisted","type":"bool"}],"name":"setWhitelisted","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"fromToken","type":"address"},{"internalType":"address","name":"toToken","type":"address"},{"internalType":"uint256","name":"fromAmount","type":"uint256"},{"internalType":"uint256","name":"minToAmount","type":"uint256"},{"internalType":"address payable","name":"to","type":"address"},{"internalType":"address","name":"rebateTo","type":"address"}],"name":"swap","outputs":[{"internalType":"uint256","name":"realToAmount","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"fromToken","type":"address"},{"internalType":"address","name":"toToken","type":"address"},{"internalType":"uint256","name":"fromAmount","type":"uint256"}],"name":"tryQuerySwap","outputs":[{"internalType":"uint256","name":"toAmount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"wooPool","outputs":[{"internalType":"contract IWooPPV2","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]')
woo_cross_chain_router_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_weth","type":"address"},{"internalType":"address","name":"_wooRouter","type":"address"},{"internalType":"address","name":"_sgInfo","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"refId","type":"uint256"},{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"address","name":"bridgedToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"bridgedAmount","type":"uint256"},{"indexed":false,"internalType":"address","name":"toToken","type":"address"},{"indexed":false,"internalType":"address","name":"realToToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"minToAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"realToAmount","type":"uint256"},{"indexed":false,"internalType":"uint8","name":"swapType","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"fee","type":"uint256"}],"name":"WooCrossSwapOnDstChain","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"refId","type":"uint256"},{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"address","name":"fromToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"fromAmount","type":"uint256"},{"indexed":false,"internalType":"address","name":"bridgeToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"minBridgeAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"realBridgeAmount","type":"uint256"},{"indexed":false,"internalType":"uint8","name":"swapType","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"fee","type":"uint256"}],"name":"WooCrossSwapOnSrcChain","type":"event"},{"inputs":[],"name":"ETH_PLACEHOLDER_ADDR","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"FEE_BASE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"bridgeSlippage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"claimFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"refId","type":"uint256"},{"internalType":"address payable","name":"to","type":"address"},{"components":[{"internalType":"address","name":"fromToken","type":"address"},{"internalType":"address","name":"bridgeToken","type":"address"},{"internalType":"uint256","name":"fromAmount","type":"uint256"},{"internalType":"uint256","name":"minBridgeAmount","type":"uint256"}],"internalType":"struct IWooCrossChainRouterV3.SrcInfos","name":"srcInfos","type":"tuple"},{"components":[{"internalType":"uint16","name":"chainId","type":"uint16"},{"internalType":"address","name":"toToken","type":"address"},{"internalType":"address","name":"bridgeToken","type":"address"},{"internalType":"uint256","name":"minToAmount","type":"uint256"},{"internalType":"uint256","name":"airdropNativeAmount","type":"uint256"},{"internalType":"uint256","name":"dstGasForCall","type":"uint256"}],"internalType":"struct IWooCrossChainRouterV3.DstInfos","name":"dstInfos","type":"tuple"},{"components":[{"internalType":"address","name":"swapRouter","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct IWooCrossChainRouterV3.Src1inch","name":"src1inch","type":"tuple"},{"components":[{"internalType":"address","name":"swapRouter","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct IWooCrossChainRouterV3.Dst1inch","name":"dst1inch","type":"tuple"}],"name":"crossSwap","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"dstExternalFeeRate","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feeAddr","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"stuckToken","type":"address"}],"name":"inCaseTokenGotStuck","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"refId","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"components":[{"internalType":"uint16","name":"chainId","type":"uint16"},{"internalType":"address","name":"toToken","type":"address"},{"internalType":"address","name":"bridgeToken","type":"address"},{"internalType":"uint256","name":"minToAmount","type":"uint256"},{"internalType":"uint256","name":"airdropNativeAmount","type":"uint256"},{"internalType":"uint256","name":"dstGasForCall","type":"uint256"}],"internalType":"struct IWooCrossChainRouterV3.DstInfos","name":"dstInfos","type":"tuple"},{"components":[{"internalType":"address","name":"swapRouter","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct IWooCrossChainRouterV3.Dst1inch","name":"dst1inch","type":"tuple"}],"name":"quoteLayerZeroFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_bridgeSlippage","type":"uint256"}],"name":"setBridgeSlippage","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_feeAddr","type":"address"}],"name":"setFeeAddr","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_chainId","type":"uint16"},{"internalType":"address","name":"_crossRouter","type":"address"}],"name":"setWooCrossRouter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_wooRouter","type":"address"}],"name":"setWooRouter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sgInfo","outputs":[{"internalType":"contract ISgInfo","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"},{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"bridgedToken","type":"address"},{"internalType":"uint256","name":"amountLD","type":"uint256"},{"internalType":"bytes","name":"payload","type":"bytes"}],"name":"sgReceive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"srcExternalFeeRate","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"weth","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"wooCrossRouters","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"wooRouter","outputs":[{"internalType":"contract IWooRouterV2","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]')

# Адреса смарт-контрактов
WOO_ROUTER_ADDRESS = web3.to_checksum_address('0x4c4AF8DBc524681930a27b2F1Af5bcC8062E6fB7')
WOO_CROSS_CHAIN_ROUTER_ADDRESS = web3.to_checksum_address('0xCa10E8825FA9F1dB0651Cd48A9097997DBf7615d')

# Инициализация контрактов
woo_router_contract = web3.eth.contract(address=WOO_ROUTER_ADDRESS, abi=woo_router_abi)
woo_cross_chain_router_contract = web3.eth.contract(address=WOO_CROSS_CHAIN_ROUTER_ADDRESS,
                                                    abi=woo_cross_chain_router_abi)


def generate_reference_id(length=9):
    """Генерация уникального идентификатора"""
    reference_id = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return int(reference_id)


def send_transaction(transaction, private_key):
    """Отправка транзакции в блокчейн"""
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash


def perform_swap(source_token, destination_token, amount, slippage, private_key):
    """Выполнение обычного свапа"""
    nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)
    amount_wei = web3.to_wei(amount, 'ether')
    min_amount = int(amount_wei * (1 - slippage / 100))

    transaction = woo_router_contract.functions.swap(
        source_token,
        destination_token,
        amount_wei,
        min_amount,
        WALLET_ADDRESS,
        WALLET_ADDRESS
    ).build_transaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': nonce,
    })

    tx_hash = send_transaction(transaction, private_key)
    return tx_hash


def perform_cross_chain_swap(src_token, dst_token, amount, slippage, to_address, dst_chain_id, private_key):
    """Выполнение кросс-чейн свапа"""
    airdrop_amount = 0
    ref_id = generate_reference_id()

    to_address = web3.to_checksum_address(to_address)
    src_bridge_token = web3.to_checksum_address('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')
    dst_bridge_token = web3.to_checksum_address('0x4200000000000000000000000000000000000006')

    nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)

    amount_wei = web3.to_wei(amount, 'ether')
    min_amount = int(amount_wei * (1 - slippage / 100))

    src_infos = (src_token, src_bridge_token, amount_wei, min_amount)
    dst_infos = (dst_chain_id, dst_token, dst_bridge_token, min_amount, airdrop_amount, 200000)  # dstGasForCall

    src1inch = (web3.to_checksum_address('0x0000000000000000000000000000000000000000'), b'')
    dst1inch = (web3.to_checksum_address('0x0000000000000000000000000000000000000000'), b'')

    transaction = woo_cross_chain_router_contract.functions.crossSwap(
        ref_id,
        to_address,
        src_infos,
        dst_infos,
        src1inch,
        dst1inch
    ).build_transaction({
        'chainId': web3.eth.chain_id,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': nonce,
    })
    tx_hash = send_transaction(transaction, private_key)
    return tx_hash


def execute_with_retries(func, retries=3, delay=5, *args, **kwargs):
    """Выполнение функции с повторными попытками при ошибках"""
    for attempt in range(retries):
        try:
            result = func(*args, **kwargs)
            return result
        except ValueError as e:
            error = e.args[0]
            if error['code'] == -32000:
                print(f'Error -32000: {error["message"]}. Retrying {attempt + 1}/{retries}...')
                time.sleep(delay)
            else:
                print(f'Unexpected error: {e}. Retrying {attempt + 1}/{retries}...')
                time.sleep(delay)
        except (TransactionNotFound, TimeExhausted):
            print(f'Transaction issue. Retrying {attempt + 1}/{retries}...')
            time.sleep(delay)
    raise Exception(f"Failed after {retries} attempts")


def main(source_network, destination_network, source_token, destination_token, amount, slippage, private_key):
    """Основная функция выполнения свапа"""
    source_token = web3.to_checksum_address(source_token)
    destination_token = web3.to_checksum_address(destination_token)

    if source_network == destination_network:
        tx_hash = execute_with_retries(perform_swap, 3, 5, source_token, destination_token, amount, slippage, private_key)
    else:
        to_address = input('Enter destination address: ')
        dst_chain_id = int(input('Enter destination token chain id: '))
        tx_hash = execute_with_retries(
            perform_cross_chain_swap, 3, 5, source_token, destination_token, amount, slippage, to_address, dst_chain_id, private_key
        )

    print(f"Transaction sent! Tx hash: {tx_hash.hex()}")


if __name__ == "__main__":
    WALLET_ADDRESS = input('Enter wallet address: ')
    PRIVATE_KEY = input('Enter private key: ')
    source_network = input("Enter source network: ")
    destination_network = input("Enter destination network: ")
    source_token = input("Enter source token address: ")
    destination_token = input("Enter destination token address: ")
    amount = float(input("Enter amount to swap: "))
    slippage = float(input("Enter slippage percentage: "))

    WALLET_ADDRESS = web3.to_checksum_address(WALLET_ADDRESS)

    main(source_network, destination_network, source_token, destination_token, amount, slippage, PRIVATE_KEY)
