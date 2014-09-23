#Morgue search script

#This python file will prompt the user for the location of his or her morgue
#folder, and for the name of an entity in crawl that may have killed one of 
#his or her characters. It will search the morgue for characters that were 
#killed by that entity, and display to the user the number of characters and
#their name that were killed by that entity
import re, collections, os

#First, prompt the user for the path to their morgue, and the entity that 
#killed them
#print("Enter an entity to search for characters killed by that entity:")
#user_in = input("eg: \'Sigmund\' or \'worker ant\': ")
user_in = "orc priest"

#Declaration of important variables
#path to morgue directory:
morgue_path = "C:/Users/cmentzer/Dropbox/stone_soup-tiles-0.14/morgue/" 
#counter to keep track of number of files checked
files_checked = 0 
#counter to keep track of how many hits so far
found_counter = 0
#regular expression used to find death text
began_as_text = "(Began as .+, [0-9]+.\n.+\n.+\n)"
#running list of text that will be output
output = ""

#build a list of the names of the files in the given directory
file_list = os.listdir(morgue_path)

#we are only interested in the .txt files in the directory, 
#so we build a new list with only those.
temp_list = []
for file in file_list:
	if(file.endswith(".txt") and file.startswith("morgue")):
		temp_list.append(file)
file_list = temp_list

#for each file in the list
for file in file_list:

	#read the file's contents
	file_contents=open(morgue_path+file,'r')
	lines=file_contents.read()
	charname = "".join(re.findall("morgue-([A-Za-z0-9]+)-",file))
	began_as = "".join(re.findall(began_as_text,lines))
	print(began_as)
	if(began_as.find(user_in) != -1):
		found_counter+=1
		output += (charname+'\n'+began_as+file+'\n'+'\n')
print("There are {} characters in your morgue that were killed by {}.".format(found_counter, user_in))
print("They are:\n")
print(output)

