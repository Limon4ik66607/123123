from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import start_menu
from settings import save_user_settings, load_user_settings

class SettingsStates(StatesGroup):
    waiting_for_price = State()
    waiting_for_rarity = State()
    waiting_for_collection_name = State()
    waiting_for_collection_address = State()

async def nft_settings_buy_handler(call_or_message, state: FSMContext = None):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Установить цену", callback_data="set_price"))
    keyboard.add(InlineKeyboardButton(text="Установить редкость", callback_data="set_rarity"))
    keyboard.add(InlineKeyboardButton(text="Добавить коллекцию", callback_data="add_collection"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="start_menu"))

    if isinstance(call_or_message, types.CallbackQuery):
        await call_or_message.message.edit_text("Выберите критерий для настройки:", reply_markup=keyboard)
    elif isinstance(call_or_message, types.Message):
        await call_or_message.answer("Выберите критерий для настройки:", reply_markup=keyboard)

async def set_price(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите максимальную цену:")
    await state.set_state(SettingsStates.waiting_for_price.state)

async def set_rarity(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите минимальную редкость:")
    await state.set_state(SettingsStates.waiting_for_rarity.state)
    
async def add_collection(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите название коллекции:")
    await state.set_state(SettingsStates.waiting_for_collection_name.state)

async def collection_name_received(message: types.Message, state: FSMContext):
    collection_name = message.text
    await state.update_data(collection_name=collection_name)
    await message.answer("Введите адрес коллекции:")
    await state.set_state(SettingsStates.waiting_for_collection_address.state)

async def collection_address_received(message: types.Message, state: FSMContext):
    collection_address = message.text
    user_data = await state.get_data()
    collection_name = user_data['collection_name']
    
    user_id = message.from_user.id
    settings = load_user_settings(user_id)
    
    if 'collections' not in settings:
        settings['collections'] = []
    
    settings['collections'].append({'name': collection_name, 'address': collection_address})
    save_user_settings(user_id, settings)
    
    await message.answer(f"Коллекция '{collection_name}' добавлена с адресом '{collection_address}'.")
    await state.finish()
    await nft_settings_buy_handler(message)

async def price_received(message: types.Message, state: FSMContext):
    max_price = message.text
    user_id = message.from_user.id
    settings = load_user_settings(user_id)
    settings['max_price'] = max_price
    save_user_settings(user_id, settings)
    await message.answer("Максимальная цена установлена.")
    await state.finish()
    await nft_settings_buy_handler(message)

async def rarity_received(message: types.Message, state: FSMContext):
    min_rarity = message.text
    user_id = message.from_user.id
    settings = load_user_settings(user_id)
    settings['min_rarity'] = min_rarity
    save_user_settings(user_id, settings)
    await message.answer("Минимальная редкость установлена.")
    await state.finish()
    await nft_settings_buy_handler(message)