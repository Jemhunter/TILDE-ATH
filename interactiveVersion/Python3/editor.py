#written by Jem_hunter
import os

running = True

file = open("data\data.txt", "r+")
file2 = open("data\data2.txt", "r+")

while running:
    
    file2 = open("data\data2.txt", "r+")
    inData = file2.read()
    file2.close()
    
    
    print("Enter name of deceased:")
    inp = input()
    print()
    inp = inp.replace(" ", "")
    
    if inp == "?":
        
        file2 = open("data\data2.txt", "r+")
        inData = file2.read()
        inData = inData.replace("[", "").replace(" ", "").replace("'", "").replace('"', "").replace("]", "")
        keys = inData.split(",")
        file2.close()
        
        message = ""
        for i in keys:
            message = message + str(i) + " "
        print (message)
        print ("Are curently alive")
        print ()
        
    if inp != "":

        file = open("data\data.txt", "r+")
        file.write(inp)
        file.close()

    if inp == "THIS":
        running = False

print("The program has finished so...")
file.close()
file2.close()
os.system("pause")#needs to be modified for all OS
