# schoolDiary & pzGram
My personal project for an automated School Diary based on pzGram, my library that allows the creation of Telegram Bots
## pzGram
pzGram is still in a early phase of development, so some features (like group support) are still missing

Learn more at the wiki on [my site](http://infopz.hopto.org/pzgram)
## pzGram quick start guide
In order to create a new bot, you have to initialize a bot class object:
```python
import pzgram
bot = pzgram.Bot(api_key)
```
Once this is done, you have to give to the object a dictionary containing the command and the function:

`bot.set_commands({'/try': try_function})`

In order to create a timer inside the bot, you have to do the same thing:

`bot.set_timers({60: send_hello})`

After this basic setup, you need do put down this command to start the bod:
`bot.run()`

## schoolDiary
The bot can be found on Telegram at the username @schoolDiaryBot
This bot acts like a planner, by allowing the user to write down homeworks and tests
Right now, you can perform the following actions on the bot:
* Store your homeworks ,tests and school schedule
* View and edit your commitments
* Be auto-reminded of tests, homeworks and schedule
* Save your marks, and calculate the average

## Upcoming features
* Integration with ClasseViva API
* Integration with Conofy to add commitments also on iPhone calendar
* Bringing pzGram to a beta version, adding the support for group chats
* Creaiting a wiki on my website
