**AsteriskCDReporter**
==================
Its a python script that collects caller ID, call time, call source and destination, disposition and duration from CDR database of all outbound and inbound calls from and to PSTN network. After arranging the data it sends a report of the calls and sends a tabulated email to a user defined email address.

The script uses **`MySQLdb`** to extract data from the CDR database and uses [**`HTML.py`**][1] to tabualte the data in an HTML table.

**`smtplib`** is used to send email.
**Dependencies**
------------
Apart from standard python installation, the script requires [**`HTML.py`**][1] which is already included and **`MySQLdb`** library. You can install **`MySQLdb`** as follows:

**Ubuntu/Debian:**

    apt-get install python-mysqldb

**CentOS:**

    yum install MySQL-python

**FreeBSD**

    cd /usr/ports/databases/py-MySQLdb
    make install clean

**Usage**
-----

This script is intended to be used as a cron that runs at 23:59 everyday.

**Known Issues**
------------

At the moment the script is hard-coded to do things such as:

 - Connecting to database.
 - Counting length of numbers to distinguish PSTN from SIP extensions.
   (`if` conditions under for loop under `processcdr()` function)
 - Sending authenticated email (`sendemail()` function)

**Credits**
-------

[Saad Ali][2] - Linux/BSD Admin

[Philippe Lagadec][1] - Author of HTML.py

**License**
-------

 - The script **`AsteriskCDReporter.py`** is licensed under MIT License.
 - **`HTML.py`** is licensed under CeCILL license.

  [1]: http://www.decalage.info/python/html
  [2]: https://github.com/nixknight
