import os
import json

# path that you want to save data
savePath = os.getcwd() + "/json/save.json"

# json files in savePath
jsons = os.listdir(str(os.getcwd() + "/json"))

# if there is none, pass
if jsons == []:
    print('none in jsons')
# if there are, set global variables
else:
    print("jsons filled with something")
    # set global variables.
    # set saveData as True

savingData = {
        "baud_val" : "9600",
        "camList_val" : "0",
        "comList_val" : "", # set this later
        "width":"400", # resolutionX
        "height":"400", # resolutionY
        "redOpt": "True",
        "bluOpt": "True"
              }

with open(str(savePath), "w+") as f:
    json.dump(savingData, f)
    
with open(str(savePath), 'r') as file:
    json_data = json.load(file)


print(json_data)
    