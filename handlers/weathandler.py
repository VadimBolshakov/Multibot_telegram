"""Handler for forecast weather function."""
from asyncio import sleep
from aiogram import types

from create import dp, db, logger, i18n
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from util.keyboards import main_menu, weather_period_menu, weather_volume_menu, weather_menu_local
from view import weatherview, quoteview
from models import openweather, quote, locbyip, citydata

_ = i18n.gettext


class WeatherFSM(StatesGroup):
    location = State()
    city = State()
    period = State()
    volume = State()


# @dp.message_handler(state=None)
async def select_location(message: types.Message):
    """Input location and set FSM state."""
    await message.answer(_('Enter way of location or press "Cancel" for exit'), reply_markup=weather_menu_local)
    """Set FSM state."""
    await WeatherFSM.location.set()


@dp.message_handler(content_types=[types.ContentType.TEXT, types.ContentType.LOCATION], state=WeatherFSM.location)
async def select_period(message: types.Message, state: FSMContext):
    """Get location and suggest select of forecast period."""
    if message.location is not None:
        # location = message.location.to_dict()
        # lat = location['latitude']
        # lon = location['longitude']
        async with state.proxy() as data:
            data['latitude'] = float(message.location.latitude)
            data['longitude'] = float(message.location.longitude)
        await message.delete()

    elif message.text == 'Get by IP':
        local_data = await locbyip.location_dict()
        if isinstance(local_data, dict):
            async with state.proxy() as data:
                data['latitude'] = local_data['latitude']
                data['longitude'] = local_data['longitude']
        else:
            await message.answer(local_data, reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
            logger.warning(f'Location by IP error. '
                           f'Exit weather handler user {message.from_user.first_name} (id:{message.from_user.id})')
            await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)
            return

    elif message.text == 'Enter city':
        await message.answer(_('Enter city name or press "Cancel" for exit'), reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton('Cancel')]], resize_keyboard=True))
        """Set FSM state."""
        await WeatherFSM.city.set()
        return

    elif message.text == 'Cancel':
        await message.answer(_('Cancel'), reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        logger.info(
            f'Cancel weather handler user {message.from_user.first_name} (id:{message.from_user.id})')
        await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)
        return

    else:
        await message.answer(_('I don\'t understand you'), reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        logger.info(
            f'Cancel weather handler user {message.from_user.first_name} (id:{message.from_user.id})')
        await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)
        return
    await message.answer(_('Your location has been received:\n '
                           'latitude: {lat}\n '
                           'longitude: {lon}').format(lat=str(data['latitude']), lon=str(data['longitude'])),
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer(_('Select forecast period or press "Cancel" for exit'), reply_markup=weather_period_menu)
    """Set FSM state."""
    await WeatherFSM.period.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=WeatherFSM.city)
async def input_city(message: types.Message, state: FSMContext):
    """Set city and suggest select of forecast period."""
    async with state.proxy() as data:
        data['city'] = message.text.lower().split()
    if data['city'][0] == 'cancel':
        await message.answer(_('Cancel'), reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        logger.info(
            f'Cancel weather handler user {message.from_user.first_name} (id:{message.from_user.id})')
        await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)
        return
    else:
        city_data = await citydata.location_dict(city=data['city'][0])
        if isinstance(city_data, dict):
            async with state.proxy() as data:
                data['latitude'] = city_data['latitude']
                data['longitude'] = city_data['longitude']
        else:
            await message.answer(city_data, reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
            logger.warning(f'Location by city error. '
                           f'Exit weather handler user {message.from_user.first_name} (id:{message.from_user.id})')
            await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)
            return

        await message.answer(_('Your city has been received:\n '
                               'city: {city}\n '
                               'latitude: {lat}\n '
                               'longitude: {lon}').format(city=str(data['city'][0]), lat=str(data['latitude']),
                                                          lon=str(data['longitude'])),
                             reply_markup=types.ReplyKeyboardRemove())

        await message.answer(_('Select forecast period or press "Cancel" for exit'), reply_markup=weather_period_menu)
        """Set FSM state."""
        await WeatherFSM.period.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=WeatherFSM.period)
async def input_period(message: types.Message, state: FSMContext):
    """Set forecast period and suggest volume input its."""
    period_tuple = ('current', 'hourly', 'daily')
    async with state.proxy() as data:
        data['period'] = message.text.lower().split()
    if data['period'][0] in period_tuple:
        await message.answer(_('Your period has been received:\n '
                               'period: {per}').format(per=str(data['period'][0])), reply_markup=types.ReplyKeyboardRemove())
        await message.answer(_('Enter volume forecast:'), reply_markup=weather_volume_menu)
        await WeatherFSM.volume.set()
    else:
        await message.answer(_('I don\'t understand you'), reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        logger.info(
            f'Cancel weather handler user {message.from_user.first_name} (id:{message.from_user.id})')
        await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)


@dp.message_handler(content_types=types.ContentType.TEXT, state=WeatherFSM.volume)
async def input_volume(message: types.Message, state: FSMContext):
    """Set volume of forecast of the weather."""
    volume_tuple = ('short', 'full')
    async with state.proxy() as data:
        data['volume'] = message.text.lower().split()
    if data['volume'][0] in volume_tuple:
        await message.answer(_('Your volume has been received:\n '
                               'volume: {vol}').format(vol=str(data['volume'][0])), reply_markup=types.ReplyKeyboardRemove())
        data = await state.get_data()
        latitude = data['latitude']
        longitude = data['longitude']
        period = data['period'][0]
        volume = data['volume'][0]
        land = await db.get_user_lang_db(user_id=int(message.from_user.id))
        msg = await message.answer(_('Please, Wait a second.....'), reply_markup=types.ReplyKeyboardRemove())
        answer = weatherview.weather_view(await openweather.weather_dict(message.from_user.id,
                                                                         message.from_user.first_name,
                                                                         lat=latitude,
                                                                         lon=longitude,
                                                                         lang=land,
                                                                         period=period,
                                                                         volume=volume))
        if len(answer) > 4095:
            for x in range(0, len(answer), 4095):
                await message.answer(answer[x:x + 4095])
                await sleep(0.2)
        else:
            await message.answer(answer)

        await msg.delete()

    else:
        await message.answer(_('I don\'t understand you'), reply_markup=types.ReplyKeyboardRemove())
        logger.info(
            f'Cancel weather handler user {message.from_user.first_name} (id:{message.from_user.id})')
    # await state.reset_state(with_data=False)
    await state.finish()
    await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)


if __name__ == '__main__':
    pass
