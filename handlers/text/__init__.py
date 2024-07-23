from aiogram import Dispatcher
from handlers.text.start import start
from handlers.text.nft_sale import enter_nft_sale_price, send_nft_sale_transaction
from handlers.text.nft_auction import enter_nft_auction_min_bid, enter_nft_auction_max_bid, enter_nft_auction_step_time, enter_nft_auction_step, enter_nft_auction_end_time, send_nft_auction_transaction
from handlers.inline.nft_settings_buy import set_price, set_rarity, add_collection, nft_settings_buy_handler, price_received, rarity_received, SettingsStates, collection_address_received, collection_name_received

def register_text_handler(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])

    # Sale
    dp.register_message_handler(enter_nft_sale_price, state="get_nft_sale_address")
    dp.register_message_handler(send_nft_sale_transaction, state="get_nft_sale_price")

    # Auction
    dp.register_message_handler(enter_nft_auction_min_bid, state="get_nft_auction_address")
    dp.register_message_handler(enter_nft_auction_max_bid, state="get_nft_auction_min_bid")
    dp.register_message_handler(enter_nft_auction_step_time, state="get_nft_auction_max_bid")
    dp.register_message_handler(enter_nft_auction_step, state="get_nft_auction_step_time")
    dp.register_message_handler(enter_nft_auction_end_time, state="get_nft_auction_step")
    dp.register_message_handler(send_nft_auction_transaction, state="nft_auction_end_time")
    
    dp.register_callback_query_handler(nft_settings_buy_handler, lambda c: c.data == 'nft_settings_buy')  
    dp.register_callback_query_handler(set_price, lambda c: c.data == 'set_price', state="*")
    dp.register_callback_query_handler(set_rarity, lambda c: c.data == 'set_rarity', state="*")
    dp.register_callback_query_handler(add_collection, lambda c: c.data == 'add_collection')
    dp.register_message_handler(price_received, state=SettingsStates.waiting_for_price)
    dp.register_message_handler(rarity_received, state=SettingsStates.waiting_for_rarity)
    dp.register_message_handler(collection_name_received, state=SettingsStates.waiting_for_collection_name)
    dp.register_message_handler(collection_address_received, state=SettingsStates.waiting_for_collection_address)    


