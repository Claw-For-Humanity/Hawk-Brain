import json

# info we need

# com port -- done
# baud rate -- done 
# cam port -- done
# cam resolution x -- done
# cam resolution y -- done
# select colour -- 
# x value 
# width of the push range

dictionary = {
        "baud_val" : "9600",
        "camList_val" : "0",
        "comList_val" : "", # set this later
        "width":"400", # resolutionX
        "height":"400", # resolutionY
        "redOpt": "True",
        "bluOpt": "True"
              }

json_object = json.dumps(dictionary,indent=4)

print(json_object)

with open("sample.json", "w") as outfile:
    outfile.write(json_object)
    print('done')