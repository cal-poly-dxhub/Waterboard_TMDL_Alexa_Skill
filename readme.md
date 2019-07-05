# Central Coast Water Quality Control Board TMDL Projects Alexa Skill

```
Chase Peak
Cal Poly Digital Transformation Hub
```

## Overview
The WaterboardTMDLProjects directory contains all of the necessary files in order to operate the Alexa Skill for presenting information on water quality projects. The contents are also extendable to other projects related to using an Alexa skill to report on information from a database. The following sections on specific files will explain their contributions to the program as a whole.

**PyMySQL-0.9.3.dist-info & pymysql:**
These two directories are pulled directly from the PyMySQL documentation and did not require further manipulation in order to function within this program. Future updates to the PyMySQL library could be used in place of the present version. However, inspection into the changes between versions would be of use in determining whether or not alterations to the code would be necessary.

This library was used in order to execute SQL statements in python through a cursor object. This allowed for *lambda.py* to accept input values from the user and query the associated database. More information on PyMySQL can be found [here](https://pymysql.readthedocs.io/en/latest/).

**lambda.py:**
Here is where the JSON object created by the Alexa skill is processed. It interacts with the voice commands given by the user, and returns vocal and text responses for Alexa to give. The main function is called *lambda_handler*, and this is what begins the process of interpreting an intent when the lambda function is invoked. Each of the customized intents for questions related to counting projects, for example, represent their own method within the python file. These individual methods are activated after *lambda_handler* calls *handle_intent*. For more information on the lambda function handler process, check out the [AWS Documentation](https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html).

**waterboard_tmdl_project_query.json:**
This file encompasses the properties of the Alexa Skill itself. It includes all of the code for the individual intents and slots that Alexa needs to answer the pre- defined questions about TMDL projects.

**rds\_config.py:**
This file contains the constant values related to the AWS RDS that was used for this program. Those values are then accessed within *lambda.py* in order to create a PyMySQL cursor object.

## Getting the code into AWS
In order to get this Alexa skill functional, both the AWS Developer Center and Alexa Developer Portal need to be utilized from [here](https://developer.amazon.com). I'll break down both of these areas to show where the given code goes, and how it can be supplemented by the Alexa Developer Console.

- **Alexa Developer Console:**
\
Each of the individual intent-related functions in *lambda.py* also appear  as Intents in the Alexa Skill. Here, the slots are determined based on what  user inputs are to be expected, and according to what values are needed for database queries.
\
For determining certain database columns to access, it may be helpful to  establish hard-coded values for a slot under the Slot Type drop-down menu in *Build* mode. This can also be found under *"types"* on line 91 from *waterboard_tmdl_projectquery.json*. For example, I created an *Approval Entity* Slot Type to serve the purpose of determining the approval body (e.g. USEPA, State Board) that the user identifies in their question. The values are the spoken names of each approval board, the ID's were the column names within the database, and the synonyms offer more ways for the user to identify a specific approval body. The use of this trick can be found in the *get_approval_date* method from *lambda.py*. Lines 132-134 show variables holding information stored by these hard-coded values. By doing this, you can extract the column names or a specific piece of text from the JSON object that you automatically receive from your Alexa skill.
\
For more information, you can follow the tutorial for making an Alexa Skill at this [link](https://developer.amazon.com/en-US/alexa/alexa-skills-kit/tutorials).

- **AWS Developer Center:**
\
Within this portal, access the Lambda function service and create a function. from there, upload this zipped directory under the *Function code* window on the lambda function page. Then, connect the Alexa Skill to this lambda function by selecting *Alexa Skills Kit* from the triggers at the top of the page, and enter the Skill ID found under *Endpoint* in the Alexa Developer Portal. At this point, the lambda function is equipped with the necessary code to execute, and a connection to its corresponding front-end Alexa Skill.
\
The last two tasks to complete involve giving the lambda function an execution role and a network to operate on. 

  - Execution Role:
This step involved defining an execution role to define the permissions of the lambda function. [Here](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html) is a step-by-step tutorial from AWS  Documentation for establishing a role.

  - Network:
The last step involves establishing a network for the lambda function to work on. By choosing a VPC, you're then prompted to select subnets and security groupsfor the lambad function. These are integral for connecting the lambda function with other web services on your VPC. More information and supplementary material can be found at \[[1](https://docs.aws.amazon.com/lambda/latest/dg/vpc-rds.html)\] or \[[2](https://docs.aws.amazon.com/lambda/latest/dg/vpc.html)\].

Once all of these components to the program are in working condition, and the database is established (not described in this readme, but if you're curious, check [this](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateDBInstance.html) out), then the program should offer a structure for answering user-input questions about data from a database. In turn, *lambda.py* has the building blocks to recieve and then create vocal and text responses to those questions.

For any further questions, contact Chase Peak at **cpeak@calpoly.edu**.
