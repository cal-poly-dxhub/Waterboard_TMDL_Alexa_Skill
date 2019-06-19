```
Chase Peak
Cal Poly Digital Transformation Hub
06-19-2019
```

**Central Coast Water Quality Control Board TMDL Projects Alexa Skill**
- **Overview**\
\
The WaterboardTMDLProjects directory contains all of the necessary files in \
order to operate the Alexa Skill for presenting information on water quality \
projects. The following sections on specific files will explain their \
contributions to the program as a whole.

PyMySQL-0.9.3.dist-info & pymysql:\

These two directories are pulled directly from the internet, and did not \
require further manipulation in order to function within this program. \
Future updates to the PyMySQL library could be used in place of the present \
version. However, inspection into the changes between versions would be of \
use in determining whether or not alterations to the code would be necessary. \

This library was used in order to execute SQL statements in python through \
a cursor object. This helped *lambda.py* to accept input values from the user \
and query the associated database. More information on PyMySQL can be found \
[here](https://pymysql.readthedocs.io/en/latest/).

lambda.py:

blah blah blah

rds\_config.py:

This file contains the constants necessary to create a PyMySQL cursor object.


**Getting the code into AWS**

...
