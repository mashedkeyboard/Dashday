# Dashday
[![Build Status](https://travis-ci.org/mashedkeyboard/Dashday.svg?branch=master)](https://travis-ci.org/mashedkeyboard/Dashday)

Your day's dashboard, printed.

## What is Dashday?
Dashday is a project designed to print a wonderful summary of your day ahead on any thermal or dot matrix printer (receipt printer to those uninitiated) that supports the Epson standard [ESC/POS](https://reference.epson-biz.com/modules/ref_escpos/index.php?content_id=2).

## What does Dashday use?
Dashday is written in **Python 3.5**, and uses the wonderful [Meteocons](http://www.alessioatzeni.com/meteocons/) and [python-escpos](https://github.com/python-escpos/python-escpos) library.

## What prerequisites are there?
* A USB ESC/POS compatible thermal or dot matrix printer
* [Python 3.5](https://www.python.org/downloads/) or later
* [Pip, the Python package manager](https://pip.pypa.io/en/stable/installing/)

## How do I work this thing?
1. `git clone https://github.com/mashedkeyboard/Dashday.git dashday`
2. `cd dashday/dashday`
3. `pip install -r requirements.txt`
4. `cp dashday.cfg.sample dashday.cfg`
5. Add your own values into dashday.cfg - remember to get the Met Office API key from their [DataPoint](https://www.metoffice.gov.uk/datapoint) site. To find your printer's vendor and product IDs, [use the python-escpos documentation](https://python-escpos.readthedocs.io/en/latest/user/usage.html#usb-printer). Note that at this time Dashday only supports USB printers.
6. Run dashday.py! It should (hopefully) print out your report.

## Is that it?
Nope. More features are coming very soon to the report, it won't just be the weather :)

## What if something goes wrong?
1. Make sure you a) have dashday.cfg in your directory, and b) it's syntactically valid (check the sample to make sure).
2. Check dashday.log - see if there's anything helpful in there, it should all be human readable.
3. [Create an issue on GitHub](https://github.com/mashedkeyboard/Dashday/issues) if you still can't get things working. Include your dashday.log file.
