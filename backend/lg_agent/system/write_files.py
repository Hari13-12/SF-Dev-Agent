import os
import re
from lg_agent.core.state_model import State

# from file_tracking import update_snapshot, detect_changes

# obj_dir = "D:/Shi-SF-Agent/saleforce-Agent/org_2/force-app/main/default/objects"

def write_xml_files(state: State) -> str:
    print("Write XML Files Function Invoked")
    try:
        try:
            obj_name =  state["obj_name"]
        except Exception as e:
            print("No obj name found in state", str(e))
            obj_name = None
        # obj_dir = state["obj_dir"]
        obj_dir = "D:/Shi-SF-Agent/saleforce-Agent/org_2/force-app/main/default/objects"
        os.chdir(obj_dir)
        print("Current working directory:", os.getcwd())
        print("Writing XML files based on generated response...")
        chat_text = state["xml_content"]
        if obj_name is None:
            file_name_pattern_1 = r"[a-zA-Z]+__c\.object-meta\.xml"
            file_names_1 = re.findall(file_name_pattern_1, chat_text)
        
            file_name_pattern_2 = r"[a-zA-Z]+__c\.field-meta\.xml"
            file_names_2 = re.findall(file_name_pattern_2, chat_text)
            file_xml_dict = {}
            for i in file_names_1 + file_names_2:
                s = chat_text.find(i)
                start = chat_text.find("```xml", s)
                end = chat_text.find("```", start + 6)
                file_xml_dict[i] = chat_text[start + 6:end]
        else:
            file_name_pattern_2 = r"[a-zA-Z]+__c\.field-meta\.xml"
            file_names_2 = re.findall(file_name_pattern_2, chat_text)
            file_xml_dict = {}
            for i in file_names_2:
                s = chat_text.find(i)
                start = chat_text.find("```xml", s)
                end = chat_text.find("```", start + 6)
                file_xml_dict[i] = chat_text[start + 6:end]

    
        dict = file_xml_dict
        if obj_name is None:
            try:
                print("Started creating new object and writing object file...")
            # Navigating to objects directory
                os.chdir(obj_dir)
                obj_folder = next(iter(dict))
                obj_folder = obj_folder.replace(".object-meta.xml","")
            # Creating directory for the new object and navigating to it
                os.mkdir(obj_folder)
                os.chdir(obj_folder)
                print("Current_Dir for object:",os.getcwd())
                for k, v in dict.items():
                            key = k
                            value = v
                            break
                clean_value = value.lstrip()

                if clean_value.strip():  # ensure not empty
                    with open(key, 'w', encoding="utf-8") as file:
                        file.write(clean_value)
                print(f"Created folder for object: {obj_folder} and written object file.")
        
                print("Started creating field files...")
                os.mkdir("fields")
                os.chdir("fields")
                print("Current_Dir for fields:",os.getcwd())
                for index, (key, value) in enumerate(dict.items()):
                    if index >= 1:
                        clean_value = value.lstrip()
                        if clean_value.strip():  # ensure not empty
                            with open(key, 'w', encoding="utf-8") as file:
                                file.write(clean_value)
                print(f"Field files created successfully for object: {obj_folder}")
                # print("Dirctory changed back to objects folder:",obj_dir)
            # changes, current_files = detect_changes()

            # if not changes:
            #     print("No files modified")
            # else:
            #     print(json.dumps(changes, indent=2))

            # print("\n--- End of Report ---\n")

            # # After user approves changes
            # update_snapshot(current_files)
                state["response"] = f"Files created successfully for object: {obj_folder}"
                # return f"Files created successfully for object: {obj_folder}"
            except Exception as e:
                # print("Exception occurred during field file creataion", str(e))
                state["response"] = f"Exception occurred during field file creataion : {str(e)}"

        else:
            print("Started writing field files for existing object...")
            fields_path = os.path.join(obj_dir, state["obj_name"], "fields")
            os.chdir(fields_path)

            print("Current working directory for fields:", os.getcwd())
            for k, v in dict.items():
                key = k
                value = v
                clean_value = value.lstrip()

                if clean_value.strip():  # ensure not empty
                    with open(key, 'w', encoding="utf-8") as file:
                        file.write(clean_value)
            print(f"Field files updated successfully for object: {state['obj_name']}")
            state["response"] = f"Field files updated successfully for object: {state['obj_name']}"
            # return f"Field files updated successfully for object: {state['obj_name']}"   
    except Exception as e:
        print("Exception occurred during file writing process", str(e))
        # return f"Exception occurred during file writing process : {str(e)}"
        state["response"] = f"Exception occurred during file writing process : {str(e)}"
    return state
        
        
# xml_response_1 = """
# 1. File Name: `Invoice__c.object-meta.xml`
# ```xml
# <?xml version="1.0" encoding="UTF-8"?>
# <CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
#     <label>Invoice</label>
#     <pluralLabel>Invoices</pluralLabel>
#     <nameField>
#         <label>Invoice Name</label>
#         <type>Text</type>
#     </nameField>
#     <deploymentStatus>Deployed</deploymentStatus>
#     <sharingModel>ReadWrite</sharingModel>
# </CustomObject>
# ```

# 2. File Name: `Invoice_Number__c.field-meta.xml`
# ```xml
# <?xml version="1.0" encoding="UTF-8"?>
# <CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
#     <fullName>Invoice_Number__c</fullName>
#     <label>Invoice Number</label>
#     <type>Text</type>
#     <length>30</length>
#     <required>false</required>
#     <unique>false</unique>
# </CustomField>
# ```
# """

# xml_response_2 = """
# 1. File Name: `Amount__c.field-meta.xml`
# ```xml
# <?xml version="1.0" encoding="UTF-8"?>
# <CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
#     <fullName>Amount__c</fullName>
#     <label>Amount</label>
#     <type>Currency</type>
#     <precision>18</precision>
#     <scale>2</scale>
#     <required>false</required>
# </CustomField>
# ```

# 2. File Name: `Due_Date__c.field-meta.xml`
# ```xml
# <?xml version="1.0" encoding="UTF-8"?>
# <CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
#     <fullName>Due_Date__c</fullName>
#     <label>Due Date</label>
#     <type>Date</type>
#     <required>false</required>
# </CustomField>
# ```
# """

# write_xml_files(obj="Invoice__c",xml_response=xml_response_2)
# # write_xml_files(xml_response=xml_response_1)
