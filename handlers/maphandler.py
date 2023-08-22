"""Handler for locations function."""

from aiogram import types
from create import dp, db, logger, i18n
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from util.keyboards import main_menu, map_menu
from view import quoteview
from models import quote, locbyip

_ = i18n.gettext


class MapsFSM(StatesGroup):
    location = State()


# @dp.message_handler(state=None)
async def select_location(message: types.Message):
    """Input location and set FSM state."""
    await message.answer(_('Enter way of location or press "Cancel" for exit'), reply_markup=map_menu)
    """Set FSM state."""
    await MapsFSM.location.set()


@dp.message_handler(content_types=[types.ContentType.TEXT, types.ContentType.LOCATION], state=MapsFSM.location)
async def select_period(message: types.Message, state: FSMContext):
    """Get location and show map or location data."""
    if message.location is not None:
        # location = message.location.to_dict()
        # lat = location['latitude']
        # lon = location['longitude']
        async with state.proxy() as data:
            data['latitude'] = float(message.location.latitude)
            data['longitude'] = float(message.location.longitude)
        await message.answer(_('Your location has been received:\n '
                               'latitude: {lat}\n '
                               'longitude: {lon}').format(lat=data['latitude'], lon=data['longitude']),
                             reply_markup=types.ReplyKeyboardRemove())

        await db.add_request_db(user_id=message.from_user.id, type_request='location',
                                num_tokens=1, status_request=True)
        logger.info(
            f'Exit from location handler user {message.from_user.first_name} (id:{message.from_user.id})')

    elif message.text == 'Get by IP':
        local_data = await locbyip.location_dict()
        if isinstance(local_data, dict):
            await message.answer(_('Your location has been received:\n'
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

            await db.add_request_db(user_id=message.from_user.id, type_request='location',
                                    num_tokens=0, status_request=True)
            logger.info(
                f'Exit from location handler user {message.from_user.first_name} (id:{message.from_user.id})')

        else:
            await message.answer(local_data, reply_markup=types.ReplyKeyboardRemove())

    else:
        await message.answer(_('I don\'t understand you'), reply_markup=types.ReplyKeyboardRemove())
        logger.info(
            f'Cancel map handler user {message.from_user.first_name} (id:{message.from_user.id})')
    await state.finish()
    await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)


if __name__ == '__main__':
    pass
