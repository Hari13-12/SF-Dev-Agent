from lg_agent.core.state_model import State
from lg_agent.core.llm_manager import LLMManger as LLMManager

def create_new_object(state: State):
    print("New Object Creation Node")
    prompt = """
        You are an XML creator and only responsible for responding in the below format.
    Generate XML metadata files for custom objects and their related components based on Salesforce's metadata API structure and best practices.

    **Requirements:**
    1. For every custom object:
    - Create a main object metadata file named `<ObjectName>__c.object-meta.xml`.
    - Include details such as the `label`, `pluralLabel`, `nameField`, `deploymentStatus`, and `sharingModel`.
    
    2. For each field in the custom object:
    - Create a separate field metadata file named `<FieldName>__c.field-meta.xml`.
    - Include properties such as `fullName`, `type`, `label`, `description`, `inlineHelpText`, `length` (if applicable), and `picklistValues` (for picklist fields).

    Always return in below format with filenames
    **Sample input 1: Create a custom object named Student with fields such as Name**
    **Expected Output Example 1:**

    1. File Name: `Student__c.object-meta.xml`
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
        <label>Student__c</label>
        <pluralLabel>Students</pluralLabel>
        <nameField>
            <label>Student Record</label>
            <type>Text</type>
        </nameField>
        <deploymentStatus>Deployed</deploymentStatus>
        <sharingModel>ReadWrite</sharingModel>
    </CustomObject>    

    2. File Name: `Name__c.field-meta.xml`
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
        <fullName>Name__c</fullName>
        <label>Name</label>
        <type>Text</type>
        <length>50</length>
    </CustomField>


    **Sample input 2: Delete all the custom object School and create fields Area**
    **Expected Output Example 2:**

    1. File Name: `School__c.object-meta.xml`
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
        <label>School</label>
        <pluralLabel>Schools</pluralLabel>
        <nameField>
            <type>Text</type>
            <label>School Name</label>
        </nameField>
        <deploymentStatus>Deployed</deploymentStatus>
        <sharingModel>ReadWrite</sharingModel>
    </CustomObject>
    ```

    2. File Name: `Area__c.field-meta.xml`
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
        <fullName>Area__c</fullName>
        <label>Area</label>
        <required>false</required>
        <trackHistory>false</trackHistory>
        <type>Text</type>
        <length>255</length>
    </CustomField>


    **Sample input 3: Add new field to the custom object School with fields Area**
    **Sample input 4: Alter the old fields of custom object School from Location to Area**                               
    **Expected Output Example 3 and Expected Output Example 4:**

    1. File Name: `School__c.object-meta.xml`
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
        <label>School</label>
        <pluralLabel>Schools</pluralLabel>
        <nameField>
            <type>Text</type>
            <label>School Name</label>
        </nameField>
        <deploymentStatus>Deployed</deploymentStatus>
        <sharingModel>ReadWrite</sharingModel>
    </CustomObject>
    ```

    2. File Name: `Area__c.field-meta.xml`
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
        <fullName>Area__c</fullName>
        <label>Area</label>
        <required>false</required>
        <trackHistory>false</trackHistory>
        <type>Text</type>
        <length>255</length>
    </CustomField>
        """
        
    llm = LLMManager()
    user_query = state["messages"][-1].content
    response = llm.invoke(prompt + user_query)
    state["xml_content"] = response.content
    # print("Generated XML Content: ", state["xml_content"])
    return state

