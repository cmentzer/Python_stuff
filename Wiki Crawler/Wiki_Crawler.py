#Python web parsing
#The purpose of this script is to navigate the M-AT wiki
#and create snippets automatically from the function definitions there.

# ---- Outline ---- #
#This script is a rough implementation attempting to automate the creation
#of sublime-text 3 Snippets for commonly used M-AT functions. This outline
#will briefly attempt to explain the process through which that automation 
#takes place, and will serve as an area for keeping track of ideas for 
#future improvement. 

#The script makes use of the MEDITECH M-AT Wiki found at stxwiki.meditech.com
#As such, the first step the script takes is to request the HTML source for
#the main page of the wiki and build a list of the outgoing hyperlinks from 
#that page. It then uses these outgoing hyperlinks to "find" the pages
#for each of the component groups. 

#As an example of this, we will look at the #WebComponents group of functions, 
#which is the first group that this script builds snippets for. 

#The script finds the hyperlink to the #WebComponents page and requests the 
#source for that page before building a list of the links to the detail pages
#of each of the components, in much the same was as above. The script then
#iterates over that list, "visiting" each component's detail page by requesting
#the page's source code. For each page, the script parses the source code
#and finds the function's parameters (which are conveniently represented as
#even more hyperlinks)

#Collecting these parameters into seperate lists (components for the parameter, 
#and values for the type definitions of those parameters), the script formats
#a block of plain text that represents the function and writes that plain text
#to a file input.txt (this may seem confusing: This script outputs plaintext to
#a file called input.txt, which is then used as input to a second script). 

#Once all of the functions for a specfic group (e.g. #WebComponents) have been
#parsed and stored as plaintext in input.txt, the script will move on the the 
#next group (e.g. #ScreenComponents). Once all of the groups have been parsed, 
#the script calls Snippet_Generation.py's Main function. Documentation for
#Snippet_Generation.py can be found within the source code for that script. 

# ---- TODO ---- #
# - Prompt user for output directory, or make the script build snippets in the
#	same directory that the script is being executed from. 
# - Format plaintext output so that columns line up nicely
def main():
	import sys, re, collections, os, urllib.request, Snippet_Generation

	#Abstracted function that builds the plaintext output
	def build_output(function_name, function_components, function_values):
		#Build the string that will be written to the file (plain text, will be used to build XML)
		output_array = []
		output_array.append("<a>"+function_name+"\n")
		output_array.append("\t\t <b>:"+function_name+"\t\t\t\t"+"${1:Name}\n")
		i = 0
		while i < len(function_components) and i < len(function_values):
			 output_array.append("\t\t "+function_components[i]+"\t\t\t\t${"+str(i+2)+":"+function_values[i]+"}\n")
			 i+=1
		output_array.append("</b>\n")
		output_array.append("<tabTrigger>:"+function_name+"</tabTrigger>\n")
		output_array.append("<description>"+function_name+"</description>\n\n")
		output_array.append("-----------------------------------------------------------\n")
		return("".join(output_array))

	#Declaration of permanent variables
	#Path to starting URL
	initial_url = "http://stxwiki.meditech.com"
	#the source variable contains the HTML source for the current URL
	source = ""

	#Open the page at the initial url and read the source code into source
	page = urllib.request.urlopen(initial_url+"/wiki11/Main_Page")
	source = page.read()

	#convert page souce to plain text
	safe_source = str(source, encoding='cp1252', errors='ignore')
	page.close()

	#Pull all of the clickable links out of the source code
	hrefs = re.findall("<a href=\"(.+?)\" title.+?</a>&#160",safe_source)

	#Hard code the supported sections of the wiki
	sections = []
	sections.append("X-BodyButtons")
	sections.append("X-Conversion")
	sections.append("X-DataDef")
	sections.append("X-DataType")
	sections.append("X-Dustributed Processing")
	sections.append("X-Footer")
	sections.append("X-Graph")
	sections.append("X-Header")
	sections.append("X-Iconset")
	sections.append("X-ImportExport")
	sections.append("X-Include")
	sections.append("X-Locals")
	sections.append("X-Magic")
	sections.append("X-Menu")
	sections.append("X-Preamble")
	sections.append("X-Report")
	sections.append("X-ReportFrame")
	sections.append("X-Screen")
	sections.append("X-ScreenComponent")
	sections.append("X-ScreenPage")
	sections.append("X-ScreenRecord")
	sections.append("X-ScreenStyle")
	sections.append("X-Search")
	sections.append("X-SearchRecords")
	sections.append("X-Toolset")
	sections.append("X-Translation")
	sections.append("X-Webcomponent")
	sections.append("X-WebRegion")
	sections.append("X-WebRoutine")
	sections.append("X-WebStyle")
	sections.append("X-WebValidation")

	#Hard code the regular expression that is used to find the desired urls in each section 
	section_regexs = sections
	#The current section number: 
	index = 0


	#First, we need to setup the file that we will write data from the web to. This file
	#will then be used as input to the second script of this process, which will generate
	#the snippets. 

	#Output to the input file that will be used in the other script
	output_path = os.path.dirname(os.path.realpath(sys.argv[0]))+"\input.txt"

	#Empty the output file and print an opening line to the top of that file
	firstLine = "<!--- Text generated by python script. --->\n"
	file = open(output_path,'w')
	file.write(firstLine)
	file.close()


	for section in sections:
		# ---- First, get all of the WebComponents and make snippets for them.
		# ---- This section will also perform some setup steps that will not 
		# ---- be repeated in other sections

		#Find the link to the #Webcomponenets page
		for link in hrefs:
			x=re.findall("("+section+")",link)
			if(x==[section]):
				desired_link = link
				break
		#Go to the found page, and get its source
		print(initial_url+desired_link)
		page = urllib.request.urlopen(initial_url+desired_link)
		source = page.read()

		#convert page souce to plain text
		# --- NOTE --- #
		#Encoding = 'cp1252': I'm not sure what the deal is with this.
		#It is necessary to do because the source code that is imported by page.read()
		#is encoding using 'cp1252' a format which contains symbols that the windows
		#cmd line (python compiler) cannot interpret. As such the source is considered a 
		#byte-like object by the compiler rather than a string, and we cannot use regular
		#expressions (necessary for re.findall()). To rectify this, we must convert the 
		#source to a string using the str() function, passing in the current encoding
		#so that the function knows what decoding to use. 
		safe_source = str(source, encoding='cp1252', errors='ignore')
		page.close()

		#Pull all of the clickable links out of the source code
		component_links = re.findall("<li><a href=\"(.+?)\" title.+?</a>",safe_source)

		#remove unwanted links
		component_links_temp = []
		for link in component_links:
			#This can be abstracted to allow us to use the same code for multiple groups,
			#rather than having X-WebComponent (or any other group) hard-coded. 
			x=re.findall("("+section_regexs[index]+")",link)
			if(x==[section_regexs[index]]):
				#This temp list contains only the elements we want.
				component_links_temp.append(link)

		component_links = component_links_temp

		#for each of the component links we need to navigate to that page and its information
		#to a temporary file, from which snippets will be generated. 
		for link in component_links:
			#Go to the found page, and get its source
			print(initial_url+link)
			page = urllib.request.urlopen(initial_url+link)
			source = page.read()
			#convert page souce to plain text
			safe_source = str(source, encoding='cp1252', errors='ignore')
			page.close()

			#get the name of the function
			name = re.findall("<td>&#160;:([a-zA-Z]+?)</td>",safe_source)
			name = name[0]
			#find all of the parameters to this funtion, and their types. 
			components = re.findall("&#160;&#160;<a href=\"#(.+?)\".+?</a></td>",safe_source)
			values = re.findall("<td style=\"padding-left:5px; text-align:left;\">([a-zA-Z/]+?)</td>",safe_source)

			#Build the string that will be written to the file (plain text, will be used to build XML)
			output = build_output(name, components, values)

			#Re-open the file to append the data to the end of it. 
			file = open(output_path,'a')
			file.write(output)
			file.close()
		index+=1

	#Call the second script which will build the snippets
	Snippet_Generation.main()
