import os
import json

cmd0= "cat /var/log/lsc/lsc.log | grep 'Starting\ LSC' > outfile.txt"
os.system(cmd0)

with open('outfile.txt') as f:
    mylist = [line.rstrip('\n') for line in f]

txt=mylist.pop()
x = txt.split()


cmd1="cat /var/log/lsc/lsc.log | grep -A 1000 " + x[0] + '\ ' + x[1] + " > log.txt"
os.system(cmd1)

cmd2="cat log.txt | grep ', errors: ' | awk '{print $19}' > errors.txt"
os.system(cmd2)

cmd3="cat log.txt | grep 'ERROR - Error' | awk '{print $11}'| awk -F',' '{print $1}' | sort -u | awk -F'=' '{print $2}'> users.txt"
os.system(cmd3)

with open('errors.txt') as f:
    mylist1 = [line.rstrip('\n') for line in f]

with open('users.txt') as f:
    mylist2 = [line.rstrip('\n') for line in f]

if mylist1[0] == '0' and mylist1[1] == '0':
    result = {"result": "OK"}
    print(result)

else:
    result = {"result": "NOT OK"}
    result["users"] = []
    result.update({"users": mylist2 })
    result = json.dumps(result, indent=4)    
    print(result)


file = open("/var/www/html/result","w")
file.write(str(result))
