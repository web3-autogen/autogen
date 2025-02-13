from autogen_core.tools import FunctionTool
from web3 import Web3

# Initialize Web3 connection (defaulting to Infura, but can be customized)
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))


def call_web3_function(
    contract_address: str, abi: list, function_name: str, args: list = None
) -> str:
    try:
        if not w3.is_connected():
            return "Error: Web3 provider not connected"

        # Load the contract
        contract = w3.eth.contract(address=contract_address, abi=abi)

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
    description="Calls a function on an Ethereum smart contract using Web3.",
    func=call_web3_function,
    global_imports=["web3"],
)
