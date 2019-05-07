import rds_config
import traceback
import pymysql
import random
import sys

#rds settings
RDS_HOST  = rds_config.db_endpoint
PASSWORD = rds_config.db_password
NAME = rds_config.db_username
DB_NAME = rds_config.db_name
TABLE_NAME = "project"

"""
constant keywords used within queries to access values.
These may include specific column names, for example.
"""
#column that contains a string of the name of a TMDL project
project_name_col = "Project_Name"

#column that contains a single string of all of the sources of a TMDL project
sources_col = "Sources"

#column that contains a string/date object of the completion date for a TMDL project
completion_date_col = "TMDL_completion_date"

reprompt_texts = ["Is there anything else that I can help with?", 
                  "What other questions do you have?", "Anything else?",
                  "What else can I do for you?"]

try:
    conn = pymysql.connect(RDS_HOST, user = NAME, passwd = PASSWORD, db = DB_NAME,
        connect_timeout=5, port = 3306)
except:
    print("ERROR: Could not connect to MySQL instance.")
    sys.exit()

"""
event: The event object, describing type and attributes of the event
context: The context for which the event occured
return: speech and card info for alexa
"""
def lambda_handler(event, context):
    try:
        if event['request']['type'] == "LaunchRequest":
            return welcome_response()
        elif event['request']['type'] == "IntentRequest":
            return handle_intent(event['request'])
        elif event['request']['type'] == "SessionEndedRequest":
            return handle_session_end(event['request'], event['session'])
    except:
        return error_response(True)


"""
Delegates a specific intent call to other helper functions
 intent_request: intent-specific data
 return: call to intent-specific function
"""
def handle_intent(intent_request):
    try:
        intent_name = intent_request['intent']['name']
        intent_slots = intent_request['intent']['slots']
        if intent_name == "countTMDLProjects":
            return count_tmdl_sources(intent_slots)
        elif intent_name == "getApprovalDate":
            return get_approval_date(intent_slots)
        elif intent_name == "compareCompletionDate":
            return compare_completion_date(intent_slots)
        else:
            raise ValueError("Invalid intent.")
    except:
        return error_response()


"""
Cleans up after session is completed, mostly for debug
 end_request: request identification value
 session: the session associated with the end_request
"""  
def handle_session_end(end_request, session):
    card_title = "Session Ended"
    speech_output = "Waterboard data search completed."
    return build_response({}, build_speech_response(card_title, speech_output,
        speech_output, True))


"""
welcome response for initiating the alexa skill
"""
def welcome_response():
    card_title = "Welcome"
    speech_output = "Welcome to the Waterboard TMDL project data set!"
    reprompt_output = "How can I help you?"
    return build_response({}, build_speech_response(card_title, speech_output,
        reprompt_output, False))


"""
Queries the table for a count on the number of projects with a particular source
 intent_slots: the source that we are searching for
 return: response based on the results of the query
"""
def count_tmdl_sources(intent_slots):
    try:
        source = intent_slots['source']['value']
        with conn.cursor() as cur:
            select_statement = ("select count(distinct Project_Name) from " +
                DB_NAME + "." + TABLE_NAME + " where " + sources_col + " like '%" +
                source + "%';")
            cur.execute(select_statement)
            result = cur.fetchone()[0]
            speech_output = str(result) + " projects identify " + source + " as a source."
        return build_answer(speech_output)
    except:
        return error_response()

"""
Returns a date from the table corresponding to the project and selected approval entity
 intent_slots: holding the values for the project and approval_entity we're searching for
 return: response object detailing the date of approval/adoption
 
 requirements:
  - approval_entity_id refers to the name of the column of corresponding date values
  - the table columns containing the dates are saved as id's to the Slot Type ApprovalEntity
  
 Due to the limitations of Alexa, tmdl projects that contain Spanish words are
 generally not correctly identified by Alexa.
"""
def get_approval_date(intent_slots):
    try:
        #this is used to access constant values defined within the Alexa skill 
        approval_entity_info = intent_slots['entity']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']
        project_info = intent_slots['project']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']
        
        approval_entity = approval_entity_info['name']
        approval_entity_id = approval_entity_info['id']
        project_name = project_info['name']
        project_query_value = intent_slots['project']['value']
        authorization_kind = "adopted" if approval_entity == "Regional Board" else "approved"
        
        with conn.cursor() as cur:
            select_statement = ("select " + approval_entity_id + " from " +
                DB_NAME + "." + TABLE_NAME + " where " + project_name_col +
                " like '%" + project_query_value + "%' limit 1;")
            cur.execute(select_statement)
            result = cur.fetchone()[0]
            
            #handles the case where a project doesn't have an approval date by the specified entity
            if result:
                try:
                    date = result.date()
                except:
                    date_time = result.split()
                    date = date_time[0]
                speech_output = "{0} was {1} by the {2} on {3}".format(project_name,
                    authorization_kind, approval_entity, str(date))
            else:
                speech_output = "{0} has not yet been {1} by the {2}".format(project_name,
                    authorization_kind, approval_entity)
        return build_answer(speech_output)
    except:
        return error_response()

"""
Returns a count of the number of projects with a completion date before/after/on the input date
 intent_slots: contains the date to compare each project's completion date, and an 
    identifier for looking before/after the inputted date
 return: response object detailing the number of projects with a completion date
    before/after the given date

 requirements:
 -AMAZON.DATE slot type returns values for the 'date' slot in the format YYYY, YYYY-MM, or YYYY-MM-DD
"""
def compare_completion_date(intent_slots):
    try:
        date_input = intent_slots['date']['value'] #string YYYY-MM-DD or YYYY-MM or YYYY
        comparison_type = intent_slots['comparison']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
        comparison_input = intent_slots['comparison']['value']
        comparisons = {'before': '>', 'on': '=', 'after': '<'}
        comparator = comparisons.get(comparison_type) #to be used in the query
        
        #this formats the date and date comparator for the select statement based on date_input
        date_regulator = {4:['-01-01', 'YEAR'], 7: ['-01', 'MONTH'], 10: ['','DAY']}
        date = date_input + date_regulator.get(len(date_input))[0]
        calendar_comparator = date_regulator.get(len(date_input))[1]
        
        with conn.cursor() as cur:
            select_statement = ("select count(distinct " + project_name_col + 
                ") from " + DB_NAME + "." + TABLE_NAME + " where " + completion_date_col +
                " != str_to_date('0000-00-00', '%Y-%m-%d') and timestampdiff(" +
                calendar_comparator + ", " + completion_date_col + ",str_to_date('" +
                date + "' ,'%Y-%m-%d')) " + comparator + " 0;")
            cur.execute(select_statement)
            result = cur.fetchone()[0]
            speech_output = (str(result) + " projects have a completion date " +
                comparison_input + " " + date_input)
        return build_answer(speech_output)
    except:
        return error_response()


"""
Creation of the answer response object
 result: the quantitative result of the query
 speech_output: the formatted speech output
 return: response object
"""
def build_answer(speech_output):
    index = random.randint(0, len(reprompt_texts) - 1)
    return build_response({}, build_speech_response("Response:",
        speech_output, reprompt_texts[index], False))


"""
Creation of an error response object
 return: response object
"""
def error_response(should_end_session = False):
    traceback.print_exc()
    output_speech = "Sorry. I wasn't able to process your intended request."
    return build_response({}, build_speech_response("Error processing your request",
        output_speech, output_speech, should_end_session))


"""
Creation of an expected response object
 title: Card title to be displayed
 output: the speech
 should_end_session : identifies an ending sequence
 return: response object
"""
def build_speech_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {"type": "PlainText", "text": output},
        "card": {"type":"Standard", "title": title, "content": output, "text": output},
        "reprompt": {"outputSpeech": {"type": "PlainText", "text": reprompt_text}},
        "shouldEndSession":should_end_session
    }


"""
Formats the response for Alexa
 session_attributes: unchanged attributes of the current session
 speech_response: the response object
 return: wrapped response object
"""
def build_response(session_attributes, speech_response):
    return {"version": "1.0", "sessionAttributes": session_attributes,
        "response": speech_response
    }