"""Handler for forecast weather function."""
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from create import dp, db, logger, i18n
from models import openweather, quote, locbyip, citydata
from util.keyboards import create_menu_inline
from view import weatherview, quoteview

_ = i18n.gettext


class WeatherFSM(StatesGroup):
    """Class for weather FSM.

    Args:
        StatesGroup (StatesGroup):Basis class for translate FSM.

    Attributes:
        location (State): State for select way of location.
        city (State): State for input city name.
        local_telegram (State): State for get location by telegram.
        period (State): State for select forecast period.
        volume (State): State for select volume of forecast.
    """

    location = State()
    city = State()
    local_telegram = State()
    period = State()
    volume = State()


# @dp.message_handler(state=None)
async def select_location(message: types.Message, user_id: int) -> None:
    """Input location and set FSM state.

    :param message: Message object from user.
    :type message: Message
    :param user_id: User id.
    :type user_id: int

    :return: None
    :rtype: None
    """
    await message.answer(_('Enter way of location or press "Cancel" for exit'),
                         reply_markup=await create_menu_inline('weather_menu_local', user_id=user_id))
    """Set FSM state."""
    await WeatherFSM.location.set()


@dp.callback_query_handler(text='get_location', state=WeatherFSM.location)
async def get_location(callback_query: types.CallbackQuery) -> None:
    """Create menu for get telegram location.

    :param callback_query: CallbackQuery object from inline button click (callback_data equal 'get_location')
    :type callback_query: CallbackQuery

    :return: None
    :rtype: None
    """
    await callback_query.answer(_('Please, wait'))
    await callback_query.message.answer(_('Please, Press this button to get your location'), reply_markup=types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton('Local', request_location=True)]], resize_keyboard=True))
    """Set FSM state."""
    await WeatherFSM.local_telegram.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=WeatherFSM.local_telegram)
async def get_location_telegram(message: types.Message, state: FSMContext) -> None:
    """Get location by telegram and suggest select of forecast period.

    :param message: Message object from user.
    :type message: Message
    :param state: FSM state.
    :type state: FSMContext

    :return: None
    :rtype: None
    """
    async with state.proxy() as data:
        data['latitude'] = float(message.location.latitude)
        data['longitude'] = float(message.location.longitude)
    await message.delete()
    await message.answer(_('Your location has been received:\n '
                           'latitude: {lat}\n '
                           'longitude: {lon}').format(lat=data['latitude'], lon=data['longitude']),
                         reply_markup=types.ReplyKeyboardRemove())

    await message.answer(_('Select forecast period or press "Cancel" for exit'),
                         reply_markup=await create_menu_inline('weather_period_menu',
                                                               user_id=message.from_user.id))
    """Set FSM state."""
    await WeatherFSM.period.set()


# this callback query handler is not used
@dp.callback_query_handler(text='get_by_ip', state=WeatherFSM.location)
async def get_by_ip(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Get location by ip and suggest select of forecast period.

    :param callback_query: CallbackQuery object from inline button click (callback_data equal 'get_by_ip')
    :type callback_query: CallbackQuery
    :param state: FSM state.
    :type state: FSMContext

    :return: None
    :rtype: None
    """
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

    await callback_query.message.answer(_('Select forecast period or press "Cancel" for exit'),
                                        reply_markup=await create_menu_inline('weather_period_menu',
                                                                              user_id=callback_query.from_user.id))
    """Set FSM state."""
    await WeatherFSM.period.set()


@dp.callback_query_handler(text='enter_city', state=WeatherFSM.location)
async def get_by_city(callback_query: types.CallbackQuery) -> None:
    """Input city and set FSM state.

    :param callback_query: CallbackQuery object from inline button click (callback_data equal 'enter_city')
    :type callback_query: CallbackQuery

    :return: None
    :rtype: None
    """
    await callback_query.answer(_('Please, wait'))
    await callback_query.message.answer(_('Enter city name or press "Cancel" for exit'), reply_markup=types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton('Cancel')]], resize_keyboard=True))
    """Set FSM state."""
    await WeatherFSM.city.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=WeatherFSM.city)
async def input_city(message: types.Message, state: FSMContext) -> None:
    """Set city and suggest select of forecast period.

    :param message: Message object from user.
    :type message: Message
    :param state: FSM state.
    :type state: FSMContext

    :return: None
    :rtype: None
    """
    async with state.proxy() as data:
        data['city'] = message.text.lower().split()
    if data['city'][0] == 'cancel':
        await message.answer(_('Cancel'), reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        logger.info(
            f'Cancel weather handler user {message.from_user.first_name} (id:{message.from_user.id})')
        await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)),
                             reply_markup=await create_menu_inline('main_menu', user_id=message.from_user.id))
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
            await message.answer(_('Your city not found.\n '
                                   'Try another method'),
                                 reply_markup=await create_menu_inline('main_menu', user_id=message.from_user.id))
            return

        await message.answer(_('Your city has been received:\n '
                               'city: {city}\n '
                               'latitude: {lat}\n '
                               'longitude: {lon}').format(city=str(data['city'][0]), lat=str(data['latitude']),
                                                          lon=str(data['longitude'])),
                             reply_markup=types.ReplyKeyboardRemove())

        await message.answer(_('Select forecast period or press "Cancel" for exit'),
                             reply_markup=await create_menu_inline('weather_period_menu',
                                                                   user_id=message.from_user.id))
        """Set FSM state."""
        await WeatherFSM.period.set()


@dp.callback_query_handler(text=['current', 'hourly', 'daily'], state=WeatherFSM.period)
async def input_period(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Set forecast period and suggest volume input its.

    :param callback_query: CallbackQuery object from inline button click (callback_data equal name of period)
    :type callback_query: CallbackQuery
    :param state: FSM state.
    :type state: FSMContext

    :return: None
    :rtype: None
    """
    await callback_query.answer(_('Please, wait'))
    async with state.proxy() as data:
        data['period'] = callback_query.data
    await callback_query.answer(_('Your period has been received:\n '
                                  'period: {per}').format(per=str(data['period'])))
    await callback_query.message.answer(_('Enter volume forecast:'),
                                        reply_markup=await create_menu_inline('weather_volume_menu',
                                                                              user_id=callback_query.from_user.id))
    await WeatherFSM.volume.set()


@dp.callback_query_handler(text=['short', 'full'], state=WeatherFSM.volume)
async def input_volume(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Set volume of forecast of the weather.

    :param callback_query: CallbackQuery object from inline button click (callback_data equal name of volume)
    :type callback_query: CallbackQuery
    :param state: FSM state.
    :type state: FSMContext

    :return: None
    :rtype: None
    """
    await callback_query.answer(_('Please, wait'))
    async with state.proxy() as data:
        data['volume'] = callback_query.data
    await callback_query.answer(_('Your volume has been received:\n '
                                  'volume: {vol}').format(vol=str(data['volume'])))
    data = await state.get_data()
    latitude = data['latitude']
    longitude = data['longitude']
    period = data['period']
    volume = data['volume']
    land = await db.get_user_lang_db(user_id=int(callback_query.from_user.id))
    msg = await callback_query.message.answer(_('Please, Wait a second.....'), reply_markup=types.ReplyKeyboardRemove())
    answer = weatherview.weather_view(await openweather.weather_dict(callback_query.from_user.id,
                                                                     callback_query.from_user.first_name,
                                                                     lat=latitude,
                                                                     lon=longitude,
                                                                     lang=land,
                                                                     period=period,
                                                                     volume=volume))
    if len(answer) > 4095:
        for x in range(0, len(answer), 4095):
            await callback_query.message.answer(answer[x:x + 4095])
            await sleep(0.1)
    else:
        await callback_query.message.answer(answer)

    await msg.delete()
    await state.finish()
    await callback_query.message.answer(quoteview.quote_view(await quote.quote_dict(callback_query.from_user.id)),
                                        reply_markup=await create_menu_inline('main_menu', user_id=callback_query.from_user.id))


if __name__ == '__main__':
    pass
