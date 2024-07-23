from aiogram import Dispatcher
from handlers.inline.start import disconnect, tonkeeper_connect
from handlers.inline.nft_sale import enter_nft_sale_address
from handlers.inline.nft_auction import enter_nft_auction_address
from handlers.inline.menu import menu
from handlers.inline.nft_settings_buy import (
    set_price, set_rarity, nft_settings_buy_handler, 
    price_received, rarity_received, SettingsStates
)


def register_inline_handler(dp: Dispatcher):
    dp.register_callback_query_handler(disconnect, text="disconnect")
    
    dp.register_callback_query_handler(enter_nft_sale_address, text="nft_on_sale")

    dp.register_callback_query_handler(enter_nft_auction_address, text="nft_on_auction")
    
#    dp.register_callback_query_handler(enter_nft_buy_address, text="nft_on_buy")
    
    dp.register_callback_query_handler(nft_settings_buy_handler, lambda c: c.data == 'nft_settings_buy')
    
    dp.register_callback_query_handler(set_price, lambda c: c.data == 'set_price', state="*")
    
    dp.register_callback_query_handler(set_rarity, lambda c: c.data == 'set_rarity', state="*")
    
    dp.register_message_handler(price_received, state=SettingsStates.waiting_for_price)
    
    dp.register_message_handler(rarity_received, state=SettingsStates.waiting_for_rarity)

    dp.register_callback_query_handler(menu, text="menu", state="*")

    dp.register_callback_query_handler(tonkeeper_connect, lambda c: c.data.startswith("tonkeeper_button"))