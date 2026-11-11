from models import Preset, Action
import time
import subprocess as sp
import os
import webbrowser as wb

# Execute a whole preset, each action in order
def execute_preset(preset: Preset):
    for action in preset.actions:
        execute_action(action)
        if(action.delay < 0):
            print(f"Invalid negative delay for action: {action.type}")
        else:
            time.sleep(action.delay)


# Execute a single action from a preset
def execute_action(action: Action):
    try:
        if not action.target:
            print(f"Target is empty for action: {action.type}")
            return
        
        filename = os.path.basename(action.target)
        name = os.path.splitext(filename)[0]
    
        if(action.type == "app"):
            if(os.path.isfile(action.target)):
               sp.Popen(action.target)
            else:
                print(f"App not found: {name}")
                return  
            
        elif(action.type == "folder"):
            if(os.path.isdir(action.target)):
               os.startfile(action.target)
            else:
                print(f"Folder not found: {filename}")
                return
            
        elif(action.type == "file"):
            if(os.path.isfile(action.target)):
               os.startfile(action.target)
            else:
                print(f"File not found: {filename}")
                return
                
        elif(action.type == "url"):
            if(action.target.startswith("http://") or action.target.startswith("https://")):
                wb.open_new_tab(action.target)
            else:
                print(f"Invalid URL: {action.target}")
                return   
        else:
            print(f"Unsupported action type: {action.type}")
            return    
    
    except Exception as e:
     if(action.type != "url"):
        print(f"Failed to open {action.type}: {name} -", e) 
     else:
        print(f"Failed to open {action.type}: {action.target} -", e)
        