

with open("myfile.txt","w") as file_object:
    file_object.write("Hello file world!")

with open("myfile.txt","r") as file_object1:
    i = file_object1.read()
    print(i)