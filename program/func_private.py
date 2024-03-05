from datetime import datetime, timedelta
import time
from func_utils import format_number

# Place market order
def place_market_order(client, market, side, size, price, reduce_only):
    # Get position id
    account_response = client.private.get_account()
    position_id = account_response.data["account"]["positionId"]

    # Get expiration time
    server_time = client.public.get_time()
    expiration = datetime.fromisoformat(server_time.data["iso"].replace("Z", "")) + timedelta(seconds=70)

    # Place an order
    placed_order = client.private.create_order(
      position_id=position_id, # required for creating the order signature
      market=market,
      side=side,
      order_type="MARKET",
      post_only=False,
      size=size,
      price=price,
      limit_fee='0.015',
      expiration_epoch_seconds=expiration.timestamp(),
      time_in_force="FOK",
      reduce_only=reduce_only
    )

    # Return the placed order
    return placed_order


# Abort all open positions
def abort_all_positions(client):
    # cancel all orders
    closed_orders = client.private.cancel_all_orders()

    # Protect API
    time.sleep(0.5)
               
    # Get markets for reference of tick size
    markets = client.public.get_markets().data

    # Protect API
    time.sleep(0.5)

    # Get all open positions
    positions = client.private.get_positions(status="OPEN")
    all_positions = positions.data["positions"]

    # Close all open positions
    close_orders = []
    if len(all_positions) > 0:
        # Loop through all open positions
        for position in all_positions:
            market = position["market"]
            side = "SELL" if position["side"] == "LONG" else "BUY"
            price = float(position["entryPrice"])
            accept_price = price * 1.7 if side == "BUY" else price * 0.3
            tick_size = markets[market]["tickSize"]
            accept_price = format_number(accept_price, tick_size)
            
            # Place order to close position
            order = place_market_order(
                client, 
                market,
                side,
                position["sumOpen"],
                accept_price,
                True
            )

            # Append order to close orders
            close_orders.append(order)

            # Protect API
            time.sleep(0.2)

    # Return the close orders
    return close_orders