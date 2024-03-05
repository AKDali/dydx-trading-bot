from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED

if __name__ == '__main__':
  # Connect to dYdX
  try:
    print("Connecting to dYdX Client...")
    client = connect_dydx()
  except Exception as e:
    print(f"Error connecting to dYdX: {e}")
    exit(1)

  # Abort all positions
  if ABORT_ALL_POSITIONS:
    try:
      print("Aborting all positions ...")
      close_orders = abort_all_positions(client)
    except Exception as e:
      print(f"Error aborting all positions: {e}")
      exit(1)

  # Find Cointegrated Pairs
  if FIND_COINTEGRATED:
    # Construct market prices
    try:
      print("Fetching market prices, allow some time ...")
      df_market_prices = construct_market_prices(client)
    except Exception as e:
      print(f"Error fetching market prices: {e}")
      exit(1)
    
    # Store Cointegrated Pairs
    try:
      print("Storing cointegrated pairs ...")
      stores_result = store_cointegration_results(df_market_prices)
      if stores_result != "saved":
        print("Error storing cointegrated pairs")
        exit(1)
    except Exception as e:
      print(f"Error storing cointegrated pairs: {e}")
      exit(1)