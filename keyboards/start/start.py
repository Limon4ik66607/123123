from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text="💵 Выставить NFT", callback_data="nft_on_sale"),
               InlineKeyboardButton(text="💵 Выставить NFT (auction)", callback_data="nft_on_auction"),
               InlineKeyboardButton(text="💵 Купить NFT", callback_data="nft_on_buy"),
               InlineKeyboardButton(text="💵 Настройки критериев", callback_data="nft_settings_buy"),
               InlineKeyboardButton(text="❌ Отключить кошелёк", callback_data="disconnect")]

    keyboard.add(*buttons)

    return keyboard

def connect_buttons():
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text="Tonkeeper", callback_data=f"tonkeeper_button"))
                                     