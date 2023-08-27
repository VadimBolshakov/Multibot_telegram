"""Handler for locations function."""

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from create import dp, db, logger, i18n
# from weathandler import get_location_telegram, get_by_ip
from models import quote, locbyip
from util.keyboards import create_menu_inline
from view import quoteview

_ = i18n.gettext


class MapsFSM(StatesGroup):
    location = State()
    local_telegram = State()


# @dp.message_handler(state=None)
async def select_location(message: types.Message, user_id: int) -> None:
    """Input location and set FSM state."""
    await message.answer(_('Enter way of location or press "Cancel" for exit'),
                         reply_markup=await create_menu_inline('map_menu', user_id=user_id))
    """Set FSM state."""
    await MapsFSM.location.set()


@dp.callback_query_handler(text='get_location', state=MapsFSM.location)
async def get_location(callback_query: types.CallbackQuery) -> None:
    """Create menu for get telegram location."""
    await callback_query.answer(_('Please, wait'))
    await callback_query.message.answer(_('Please, Press this button to get your location'), reply_markup=types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton('Local', request_location=True)]], resize_keyboard=True))
    """Set FSM state."""
    await MapsFSM.local_telegram.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=MapsFSM.local_telegram)
async def get_location_telegram(message: types.Message, state: FSMContext) -> None:
    """Get location by telegram and suggest select of forecast period."""
    async with state.proxy() as data:
        data['latitude'] = float(message.location.latitude)
        data['longitude'] = float(message.location.longitude)

    await message.answer(_('Your location has been received:\n '
                           'latitude: {lat}\n '
                           'longitude: {lon}').format(lat=data['latitude'], lon=data['longitude']),
                         reply_markup=types.ReplyKeyboardRemove())

    await db.add_request_db(user_id=message.from_user.id, type_request='location',
                            num_tokens=0, status_request=True)
    logger.info(
        f'Exit from location handler user {message.from_user.first_name} (id:{message.from_user.id})')
    await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)),
                         reply_markup=await create_menu_inline('main_menu', user_id=message.from_user.id))
    await state.finish()


@dp.callback_query_handler(text='get_by_ip', state=MapsFSM.location)
async def get_by_ip(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Get location by ip and suggest select of forecast period."""
    await callback_query.answer(_('Please, wait'))
    local_data = await locbyip.location_dict()
    if isinstance(local_data, dict):
        async with state.proxy() as data:
            data['latitude'] = local_data['latitude']
            data['longitude'] = local_data['longitude']
    else:
        await callback_query.message.answer(local_data, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        logger.warning(f'Location by IP error. '
                       f'Exit weather handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
        await callback_query.message.answer(_('Your location was not received.\n '
                                              'Try another method'),
                                            reply_markup=await create_menu_inline('main_menu', user_id=callback_query.from_user.id))
        return

    await callback_query.message.answer(_('Your location has been received:\n'
                                          ' latitude: {lat}\n'
                                          ' longitude: {lon}\n'
                                          ' city: {city}\n'
                                          ' country: {country}\n'
                                          ' timezone: {timezone}\n'
                                          ' ip: {ip}\n'
                                          ' org: {org}\n').format(lat=local_data['latitude'],
                                                                  lon=local_data['longitude'],
                                                                  city=local_data['city'],
                                                                  country=local_data['country'],
                                                                  timezone=local_data['timezone'],
                                                                  ip=local_data['ip'],
                                                                  org=local_data['org']
                                                                  ),
                                        reply_markup=types.ReplyKeyboardRemove())

    await db.add_request_db(user_id=callback_query.from_user.id, type_request='location',
                            num_tokens=0, status_request=True)
    logger.info(
        f'Exit from location handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await state.finish()
    await callback_query.message.answer(quoteview.quote_view(await quote.quote_dict(callback_query.from_user.id)),
                                        reply_markup=await create_menu_inline('main_menu', user_id=callback_query.from_user.id))


if __name__ == '__main__':
    pass
