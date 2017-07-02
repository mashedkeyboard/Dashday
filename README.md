# Dashday is now deprecated :(
But good news! There's a bigger, better version of Dashday now! It's called Headlights, and it's open source too. It's 
available [here](https://github.com/mashedkeyboard/Headlights).

Well, what are you waiting for?

<hr />


# Dashday
[![Build Status](https://travis-ci.org/mashedkeyboard/Dashday.svg?branch=master)](https://travis-ci.org/mashedkeyboard/Dashday)[![codecov](https://codecov.io/gh/mashedkeyboard/Dashday/branch/master/graph/badge.svg)](https://codecov.io/gh/mashedkeyboard/Dashday)[![Code Issues](https://www.quantifiedcode.com/api/v1/project/5aa29b1022b647dfb31c700116b45891/badge.svg)](https://www.quantifiedcode.com/app/project/5aa29b1022b647dfb31c700116b45891)

Your day's dashboard, printed.

## What is Dashday?
Dashday is a project designed to print a wonderful summary of your day ahead on any thermal or dot matrix printer (receipt printer to those uninitiated) that supports the Epson standard [ESC/POS](https://reference.epson-biz.com/modules/ref_escpos/index.php?content_id=2).

## What does Dashday use?
Dashday is written in **Python**, and compiled against 3.5, but should work with **3.3 and upwards** or PyPy3. It uses a very slightly modified version of the wonderful [Meteocons](http://www.alessioatzeni.com/meteocons/) icon set for weather icons in the output, and the [python-escpos](https://github.com/python-escpos/python-escpos) library for printer communication.

## What prerequisites are there?
* A USB ESC/POS compatible thermal or dot matrix printer
* [Python 3.3](https://www.python.org/downloads/) or later (or [PyPy3](http://pypy.org/))
* [Pip, the Python package manager](https://pip.pypa.io/en/stable/installing/)

## How do I work this thing?
1. `git clone https://github.com/mashedkeyboard/Dashday.git dashday`
2. `cd dashday/dashday`
3. `pip install -r requirements.txt`
4. Run dashday.py and browse to localhost:9375.
5. Complete the setup with your own values. To find your printer's vendor and product IDs, [use the python-escpos documentation](https://python-escpos.readthedocs.io/en/latest/user/usage.html#usb-printer). Note that at this time Dashday only supports USB printers.

## What's all this about plugins?
All the individual sections of the report are put into plugins - you can enable or disable whatever you want within the app. Individual plugin configuration files live within the /config directory, and the plugins themselves live within the /plugins one. If you want to build a plugin, take a look at the weather plugin for an example to go on.

## Is that it?
Nope. More features are coming very soon to the report, it won't just be the weather :)

## What if something goes wrong?
1. Make sure you a) have dashday.cfg in your directory, and b) it's syntactically valid (check the sample to make sure).
2. Check dashday.log - see if there's anything helpful in there, it should all be human readable.
3. [Create an issue on GitHub](https://github.com/mashedkeyboard/Dashday/issues) if you still can't get things working. Include your dashday.log file.
