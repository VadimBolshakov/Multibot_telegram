[![Built status](.github/workflows/check_flake8.yml/badge.svg?branch=main)](.github/workflows/check_flake8.yml)  
  
# Welcome to my multi-function bot!

## Description

This is a multi-functional telegram bot.  Get weather information for the entered city or geolocation,  coordinates and map of your location,  current exchange rates,  translated text,  view news on various topics,  read jokes,  and send a request to the GPT chat.  To enter the bot,  the user must enter a password set in the environment file  .env.

## Bot menu

You can use the following commands:  
/start - start bot.  
/help - get help.  
/reset - reset bot.  You can use this command to reset the bot if the bot is in waiting mode.  
/language - change the language.  You can use this command to change language at all times.  
/toadmin - send the message to the administrator chatbot.

## Paradigm of work

The bot implements the following operating principle.  All incoming requests after the middleware  (middlewares module),  where the user’s validity is checked,  are sent to the handler  (handlers module)  for filtering.  The handler sends the corresponding request to the model  (models module)  for processing;  the view  (view module)  is used to display the result.  PostgreSQL database is used to store user data and successfully process queries.  Processing errors are recorded in a log file  (/logs/logconfig.log)  and sent to the email specified in the file  .env and to the administrator’s chat.

## Description .env file

TOKEN_BOT=token Telegram bot  
TOKEN_OPENWEATHER=token API get weather from  [https://openweathermap.org/](https://openweathermap.org/)  
TOKEN_CURRENCY=  not using  
TOKEN_NEWSAPI=  token API get the news  [https://newsapi.org/](https://newsapi.org/)  
TOKEN_GOOGLE_TRANSLATE=  token API google translate  [https://translation.googleapis.com/language/translate/v2](https://translation.googleapis.com/language/translate/v2)  
TOKEN_CURRENCYLAYER=token API get the current exchange rates  [https://currencylayer.com/](https://currencylayer.com/)  
GPT_API_KEY=  token API GPT chat  [https://platform.openai.com/](https://platform.openai.com/)  
PASSWORD=  password to enter to the bot

[admin]  
CHAT_ID=Id chat bot's  
EMAIL_SENDER=  email of the sender for sending exceptions 
EMAIL_PASSWORD=password email sender  
EMAIL_RECIPIENT=email for receiving exceptions  
ADMIN_ID=  Id admin chat bot's  (usually same as CHAT_ID)  
LOG_FILE=  path and the name log file  (for example  ./logs/logconfig.log)  
FOUL_FILE=  path and the name obscene words file  (for example  ./src/foul/foul.json)

[postgresql]  
DB_NAME=postgres  DB_USER=postgres  
DB_PASSWORD=123456  
DB_HOST=127.0.0.1  
DB_PORT=5432  
the standard-setting Postgresql database

## Sources

Weather:  [https://openweathermap.org](https://openweathermap.org/)  
Location by IP:  [https://ipinfo.io/json](https://ipinfo.io/json)   
Currency:  [https://currencylayer.com](https://currencylayer.com/)  for the English version,  [https://www.cbr-xml-daily.ru/daily_utf8.xml](https://www.cbr-xml-daily.ru/daily_utf8.xml) for the Russian version.  
Translate:  [https://translation.googleapis.com/language/translate/v2](https://translation.googleapis.com/language/translate/v2)  
News:  [https://newsapi.org](https://newsapi.org/)   
Jokes:  [https://github.com/taivop/joke-dataset](https://github.com/taivop/joke-dataset) (./src/jokes/jokes_en.json)  for the English version,  [https://github.com/Vl-Leschinskii/jokes_topics/blob/main/anek_utf8.zip](https://github.com/Vl-Leschinskii/jokes_topics/blob/main/anek_utf8.zip) (./src/jokes/jokes_ru.json)  for the Russian version.   
Quotes:  [https://forismatic.com](https://forismatic.com/)  ([https://forismatic.com/en/api/](https://forismatic.com/en/api/)  for the English version,  [https://forismatic.com/ru/api/](https://forismatic.com/ru/api/)  for the Russian version)

## Admin menu

The bot exists in the admin menu called by the command  /admin and consists of the following commands:  
/getlog  -  send the log file to the telegram,  
/getemail  -  send the log file to email,  
/getusers  -  send the id and users of this chat to the admin,  /getrequests  -  send the number of requests to admin,  
/sendall  -  send message to all users,  
/banneruser  -  ban user,  
/statusadmin  -  change status admin user.

## Internationalize your bot

### Instruction create multi-language contents

Requires Babel module  (including aiogram).
Our domain will be called  "base" (can be anything).
To begin,  create a directory named  "locales".  Then,  execute the command  "pybabel extract"  in the terminal to extract  files into the  "locales"  directory.  

- pybabel extract  .  -o locales/base.pot  Second,  create  *.po files.  E.g.  create en,  ru,  uk locales.  
- pybabel init  -i locales/base.pot  -d locales  -D base  -l en  
- pybabel init  -i locales/base.pot  -d locales  -D base  -l ru  
- pybabel init  -i locales/base.pot  -d locales  -D base  -l de  Third,  translate texts located in    locales/{language}/LC_MESSAGES/base.po  Once,  you must compile file    from  .po to  .mo using the next command  
- pybabel compile  -d locales  -D base  Now,  if you make changes to the base.po file you must update the files using update command  
-  pybabel update  -d locales  -D base  -i locales/base.pot  
see more  [https://docs.aiogram.dev/en/latest/examples/i18n_example.html](https://docs.aiogram.dev/en/latest/examples/i18n_example.html)

### Instruction create the multi-language menu

Create a file in the menu_{language}.txt format in the  ./scr/menu directory,  where  {language}  is the language code according to ISO 639-1.  
In this file,  enter the translation of the menu into the desired language in the format: "text": "translation" (see example in  ./scr/menu/menu_ru.txt).  
Restart the bot.  
The JSON file will be created automatically when the bot is launched.  
The language will be set from the bot settings,  or the language code according to ISO 639-1 code in the file  ./handlers/changelaand.py  (str:  37)  so that it appears in the bot menu.

## Additionally

The foul filter has only been working on Russian words yet.  The author doesn't know English well enough to filter the obscene English words.  file:  quote_against_foul from source  [https://aforisimo.ru/pro-mat/](https://aforisimo.ru/pro-mat/)

## Conclusion

The bot has an MIT license.  
If you want to support the project,  you can do it here:  [https://www.patreon.com/vadimbolshakov](https://www.patreon.com/vadimbolshakov)  
Contact vadimbolsh@gmail.com
