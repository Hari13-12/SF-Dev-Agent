from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
# from langchain_core.messages import SystemMessage, HumanMessage
# import json


a1 = "AIzaSyDMVV_lNVuZXxqu-m5Kw0aV-Q_yKIqGtOU"
a2 = "AIzaSyBlMSpjQHv5rL9TyPM0o6E3IvFxHjxzSwA"
a3 = "AIzaSyAFa86jRvq3ml9tO5qP0pSSST6SSJ1s9ew"
a4 = "AIzaSyBD6tLFJaM4_YNHT0LPXOfMf5IUhH0At10"
a5 = "AIzaSyDUo6eNHlRPSsdf3Yy_ci1YMlMK1A7NM2E"
a6 = "AIzaSyDKH7_dq9uR8fKP0Yu1J6nsXbdOjrD3f80"
a7 = "AIzaSyCudIv14Sl3ijNdgzkInT0Gby527Blk4LY"
a8 = "AIzaSyCAETZwYpW-iX1S9KYMCGlYNWgg9rKYR5Q"
a9 = "AIzaSyCTWQx7GYaqj0jNMsDP-kchMFXpER_QPe0"


class LLMManager:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", api_key=a9)

    def get_llm(self):
        return self.llm

    def invoke(self, message):
        return self.llm.invoke(message)


# # Initialize the LLM only once
# def get_llm():
#     if not hasattr(get_llm, "llm_instance"):
#         get_llm.llm_instance = ChatGoogleGenerativeAI(
#             model="models/gemini-2.5-flash", api_key=a2
#         )
#         print("LLM initialized")
#     return get_llm.llm_instance


# def get_intent(self, user_query: str):
#     prompt = """You are an Intent Analysis Agent.

# Your job is to analyze the user query and determine the correct intent.
# If the query represents a valid business request, return structured JSON data.
# If the query is a greeting, small talk, or unrelated, return a general response.

# Possible Intents

# 1) new_object -> User wants to create a new Salesforce object
# Examples:
# “Create a new custom object”
# “I want a new object for invoices”
# “Add a new object with fields”

# Output Format:
# {
#     "intent":"new_object",
#     "object_name":"<name_of_object>",
#     "fields":["<field1>", "<field2>", "..."]
# }

# 2) edit_object -> User wants to modify an existing Salesforce object
# Includes:
# Adding or updating fields
# Modifying relationships
# Updating existing object metadata
# Examples:
# “Add a field to Account”
# “Update Opportunity object”
# “Modify existing custom object”
# “Which objects have a Master-Detail relationship to Meter__c?”

# Output Format:
# {
#     "intent":"edit_object",
#     "object_name":"<name_of_object>",
#     "fields":["<fileds1>", "<modification2>", "..."]
# }

# 3) general -> Greetings, small talk, or unrelated queries
# Greetings, small talk, or unrelated queries
# Questions not requesting object creation or modification
# Examples:
# “Hi”
# “Hello”
# “What is Salesforce?”
# “What’s the weather?”

# Output Format:
# {
#     "intent":"general"
# }
# """
#     system_prompt = SystemMessage(content=prompt)
#     input_message = HumanMessage(content=user_query)
#     print("Invoking LLM for intent classification...")
#     # llm = get_llm()
#     response = self.llm.invoke([system_prompt, input_message])
#     response_content = response.content.replace("```json", "").replace("```", "")
#     return json.loads(response_content)


# def general_response(self, user_query:str) -> str:
#     prompt = """
#     You are a Salesforce Dev Agent.
#     Your capabilities are strictly limited to Salesforce metadata operations.
#     Rules:
#     1. If the user asks a COMMON INTRODUCTORY or CONVERSATIONAL question, such as:
#         - how are you
#         - who are you
#         - what can you do
#         - help
#         - hi / hello
#         respond with a brief, polite natural language answer describing yourself and your Salesforce capabilities.
#     2. If the user request is related to creating, modifying, or defining Salesforce custom objects or fields, respond ONLY with valid Salesforce XML metadata content.
#     Do not include explanations or extra text.

# 3. If the user request is outside Salesforce metadata operations AND not a common conversational question, respond with EXACTLY this sentence and nothing else:
# "I am not capable of it."

#     Constraints:
#     - Do NOT stay silent.
#     - Do NOT explain these rules.
#     - Do NOT mix XML with natural language.
#     - Always choose exactly one of the above response types.


#     """
#     system_prompt = SystemMessage(content=prompt)
#     input_message = HumanMessage(content=user_query)
#     print("Invoking LLM for general response...")
#     # llm = get_llm()
#     response = self.llm.invoke([system_prompt, input_message])
#     return response.content


# def generate_xml(self, user_query:str):
#     prompt = """
#     You are an XML creator and only responsible for responding in the below format.
# Generate XML metadata files for custom objects and their related components based on Salesforce's metadata API structure and best practices.

# **Requirements:**
# 1. For every custom object:
# - Create a main object metadata file named `<ObjectName>__c.object-meta.xml`.
# - Include details such as the `label`, `pluralLabel`, `nameField`, `deploymentStatus`, and `sharingModel`.

# 2. For each field in the custom object:
# - Create a separate field metadata file named `<FieldName>__c.field-meta.xml`.
# - Include properties such as `fullName`, `type`, `label`, `description`, `inlineHelpText`, `length` (if applicable), and `picklistValues` (for picklist fields).

# Always return in below format with filenames
# **Sample input 1: Create a custom object named Student with fields such as Name**
# **Expected Output Example 1:**

# 1. File Name: `Student__c.object-meta.xml`
# ```xml
# <?xml version="1.0" encoding="UTF-8"?>
# <CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
#     <label>Student__c</label>
#     <pluralLabel>Students</pluralLabel>
#     <nameField>
#         <label>Student Record</label>
#         <type>Text</type>
#     </nameField>
#     <deploymentStatus>Deployed</deploymentStatus>
#     <sharingModel>ReadWrite</sharingModel>
# </CustomObject>

# 2. File Name: `Name__c.field-meta.xml`
# ```xml
# <?xml version="1.0" encoding="UTF-8"?>
# <CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
#     <fullName>Name__c</fullName>
#     <label>Name</label>
#     <type>Text</type>
#     <length>50</length>
# </CustomField>


# **Sample input 2: Delete all the custom object School and create fields Area**
# **Expected Output Example 2:**

# 1. File Name: `School__c.object-meta.xml`
# ```xml
# <?xml version="1.0" encoding="UTF-8"?>
# <CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
#     <label>School</label>
#     <pluralLabel>Schools</pluralLabel>
#     <nameField>
#         <type>Text</type>
#         <label>School Name</label>
#     </nameField>
#     <deploymentStatus>Deployed</deploymentStatus>
#     <sharingModel>ReadWrite</sharingModel>
# </CustomObject>
# ```

# 2. File Name: `Area__c.field-meta.xml`
# ```xml
# <?xml version="1.0" encoding="UTF-8"?>
# <CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
#     <fullName>Area__c</fullName>
#     <label>Area</label>
#     <required>false</required>
#     <trackHistory>false</trackHistory>
#     <type>Text</type>
#     <length>255</length>
# </CustomField>


# **Sample input 3: Add new field to the custom object School with fields Area**
# **Sample input 4: Alter the old fields of custom object School from Location to Area**
# **Expected Output Example 3 and Expected Output Example 4:**

# 1. File Name: `School__c.object-meta.xml`
# ```xml
# <?xml version="1.0" encoding="UTF-8"?>
# <CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
#     <label>School</label>
#     <pluralLabel>Schools</pluralLabel>
#     <nameField>
#         <type>Text</type>
#         <label>School Name</label>
#     </nameField>
#     <deploymentStatus>Deployed</deploymentStatus>
#     <sharingModel>ReadWrite</sharingModel>
# </CustomObject>
# ```

# 2. File Name: `Area__c.field-meta.xml`
# ```xml
# <?xml version="1.0" encoding="UTF-8"?>
# <CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
#     <fullName>Area__c</fullName>
#     <label>Area</label>
#     <required>false</required>
#     <trackHistory>false</trackHistory>
#     <type>Text</type>
#     <length>255</length>
# </CustomField>
#     """
#     system_prompt = SystemMessage(content=prompt)
#     input_message = HumanMessage(content=user_query)
#     print("Invoking LLM for XML generation...")
#     # llm = get_llm()
#     response = self.llm.invoke([system_prompt, input_message])
#     # response_content = response.content.replace("```json", "").replace("```", "")
#     # return json.loads(response_content)
#     return response.content
