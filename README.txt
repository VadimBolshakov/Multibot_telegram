поменять пути в трех местах: .env, model.currencies and model.jokes
This is many function the Telegram bot.


there are using API www.openweather to get weather in city.
postgreSQL to save data.
API www.exchangeratesapi.io to get currency.
API www.chucknorris.io to get jokes.
The bot can send you weather in city, currency, jokes, and save your message in database.
You can use some following commands:
command /start to start bot.
command /help to get help.
command /reset to reset bot. If bot waiting mode, you can use this command to reset bot.
command /language to change language. You can use this command to change language at all times.

в программе реаализованна парадигма MVC. the all input requests processing in handlers (handlers module) and seng to model (model module).
in model module the all requests processing and send to view (view module).

in view module the all output requests processing and send to handlers (handlers module).

in handlers module the all input requests processing and send to model (model module).

in model module the all requests processing and send to view (view module).

in view module the all output requests processing and send to handlers (handlers module).

in currency module the requests processing make through two different channels because there are two different API for two languages, English and russinan
and using urllib module, not aiohttp module.

middleware description
loggin - send to chat admin

The foul filter only has been working on Russian words yet.  The author doesn't know English well enough to filter the obscene English words.
file: quote_against_foul with source https://aforisimo.ru/pro-mat/

The bot is free. If you want to support the project, you can do it here: https://www.patreon.com/vadimbolshakov


"""Instruction create multi languages (Internationalize your bot).

Requires Babel module (including aiogram)
Our domain will be called "base" (can be anything)
To begin, create a directory named "locales". Then, execute the command "pybabel extract" in the terminal to extract
 files into the "locales" directory.
    > pybabel extract . -o locales/base.pot
Second, create *.po files. E.g. create en, ru, uk locales.
    > pybabel init -i locales/base.pot -d locales -D base -l en
    > pybabel init -i locales/base.pot -d locales -D base -l ru
    > pybabel init -i locales/base.pot -d locales -D base -l de
Third, translate texts located in locales/{language}/LC_MESSAGES/base.po
Once, you must compile file from .po to .mo using the next command
    > pybabel compile -d locales -D base
Now, if you make changes to the base.po file you must update the files using update command
    > pybabel update -d locales -D base -i locales/base.pot
see more https://docs.aiogram.dev/en/latest/examples/i18n_example.html
 """