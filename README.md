dicerollingbot
==============

A little dice-rolling bot for vk.

Python 2.7

### Using non-standart libraries:

[vk](https://pypi.python.org/pypi/vk/1.5)
[mechanize](https://pypi.python.org/pypi/mechanize/)


### Starting a bot:

The bot needs your vk account to recieve/send messages, so there are two options to grant him appropriate rights:
* option 1 - run dndbot.py with two arguments - your email and password for vk
* option 2 - run it without any arguments. Then you will be prompted to give it permissions by opening a link, granting access and copying the "access token" from the link you were redirected to.


(I'm still thinking about more gentle ways of autorization)

Regardless of the way of authorization you have chosen, the bot will then ask you to provide it with file containing information about players


*File format:*


> &lt;gamemaster id>

> &lt;player 1 id> &lt;player 1 character name> &lt;player 1 STR> &lt;player 1 DEX> &lt;player 1 CON> &lt;player 1 WIS> &lt;player 1 INT> &lt;player 1 CHA>

> &lt;player 2 id> &lt;player 2 character name> &lt;player 2 STR> &lt;player 2 DEX> &lt;player 2 CON> &lt;player 2 WIS> &lt;player 2 INT> &lt;player 2 CHA>

> ...

*Example:*

> 999999
> 123456789 Foo 15 11 17 9 8 12
> 987654321 Bar 8 18 12 10 14 16

### Chat commands

**test** - prints "test successful"

**!roll** - rolls a dice. 

Examples:

*!roll* - roll a d20 dice

*!roll 3d10+4* - roll 3 d10 dice with modifier +4

*!roll 2d8* - roll 2d8 dice

*!roll 3 4 1* - roll 3 d4 dice with modifier +1

*!roll CHA* - roll a d20 dice with your character's charisma modifier (works if your character info is set in player information file)

*!roll dex+CON+wisdom* - several modifiers will be summed up

*!roll dex-2* - roll your character's DEX with -2 modifier

...and so on

**!set** - sets a stat

For player:

*!set <stat> <value>* - set your character's stat. This information won't be saved to players info file!

Example:

*!set INT 15*

For GM:

*!set <player id> <stat> <value>* - sets the particular player's character stat to new value.

Example:

*!set 123456789 cha 8*

**!get** - get a stat value

Examples:

*!get str* - prints your character's STR

*!get 123456789 int* - prints INT of that particular player.

**!info** - prints information on particular character

*!info <player id>*

If no id is specified, your character's info will be printed by default.

*!info*
