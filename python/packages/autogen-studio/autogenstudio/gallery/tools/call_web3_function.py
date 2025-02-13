import os

from autogen_core.tools import FunctionTool
from dotenv import load_dotenv
from web3 import Web3

# Load environment variables from .env file
load_dotenv()
alchemy_api_key = os.getenv("ALCHEMY_API_KEY")

# Initialize Web3 connection using Alchemy
ALCHEMY_URL = f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_api_key}"
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))


def call_web3_function(
    contract_address: str, abi: list, function_name: str, args: list = None
) -> str:
    """
    Calls a read-only function on an Ethereum smart contract using Web3 and Alchemy.

    Args:
        contract_address (str): The Ethereum contract address.
        abi (list): The ABI (Application Binary Interface) of the contract.
        function_name (str): The function name to call.
        args (list, optional): Arguments for the function. Defaults to None.

    Returns:
        str: The result of the function call.
    """

    try:
        if not w3.is_connected():
            return "Error: Web3 provider not connected"

        # Load the contract
        contract = w3.eth.contract(address=w3.to_checksum_address(contract_address), abi=abi)

        # Call the function
        if args:
            result = getattr(contract.functions, function_name)(*args).call()
        else:
            result = getattr(contract.functions, function_name)().call()

        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

# Create Web3 tool
web3_tool = FunctionTool(
    name="web3_tool",
    description="Calls a function on an Ethereum smart contract using Web3 and Alchemy.",
    func=call_web3_function,
    global_imports=["web3"],
)
