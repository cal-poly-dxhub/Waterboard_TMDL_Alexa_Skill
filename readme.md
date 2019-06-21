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
contributions to the program as a whole. \
\
PyMySQL-0.9.3.dist-info & pymysql:\
\
These two directories are pulled directly from the PyMySQL documentation and \
did not require further manipulation in order to function within this program. \
Future updates to the PyMySQL library could be used in place of the present \
version. However, inspection into the changes between versions would be of \
use in determining whether or not alterations to the code would be necessary. \
\
This library was used in order to execute SQL statements in python through \
a cursor object. This helped *lambda.py* to accept input values from the user \
and query the associated database. More information on PyMySQL can be found \
[here](https://pymysql.readthedocs.io/en/latest/). \
\
lambda.py:\
\
Here is where the JSON object created by the Alexa intent is processed. It \
interacts with all of the voice-commands given by the user, and returns vocal \
and text responses for Alexa to give. The main function is called *lambda_handler*, \
and this is what begins the process of interpreting an intent when the lambda \
function is invoked. Each of the customized intents for questions related to, \
for example, counting projects, getting approval dates, or comparing dates, \
represent their own method within the program. These individual methods are \
activated after *lambda_handler* calls *handle_intent*. \
\
rds\_config.py:\
\
This file contains the constant values related to the AWS Relational Database \
Service. Those values are then accessed within *lambda.py* in order to create \
a PyMySQL cursor object. \
\
- **Getting the code into AWS**\
\
In order to get this Alexa skill functional, both the AWS Developer Center and \
Alexa Developer Portal need to be utilized from [here](https://developer.amazon.com). I'll break down both \
of these areas to show where the given code goes, and how it can be supplemented \
by the Alexa Developer Console. \
- Alexa Developer Console: \
\
...\
\
- AWS Developer Center: \
\
Within this portal, access the Lambda function service and create a function. \
from there, the zip file containing the given files can be uploaded under the \
*Function code* window on the lambda function page. Then, connect the Alexa \
Skill to this lambda function by selecting *Alexa Skills Kit* from the triggers \
at the top of the page, and enter the Skill ID found under *Endpoint* in the \
Alexa Developer Portal. At this point, the lambda function is equipped with \
the necessary code to execute, and a connection to its corresponding front-end \
Alexa Skill. \
\
The last two tasks to complete involve giving the lambda function an execution \
role and a network to operate on. ...
