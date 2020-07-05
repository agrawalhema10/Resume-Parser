import re                                                                       #Import Required Library
import PyPDF2
import pandas as pd
def ExtractTextFromPDF(filename):
    pdfFileObject = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    n=pdfReader.numPages
    s=""
    for i in range(n):
        pageObject = pdfReader.getPage(i)
        s+=pageObject.extractText()
    return s
def parser(filename):                                                          #This function required file name whom we want to parse
   
    df = pd.read_excel('Resume Headings & Subheadings.xlsx')                   # Load Heading Dataset
    headings=df['headings']
    
    s=ExtractTextFromPDF(filename)                                             #Extract Text From PDF
    
    resume=s.split("\n")
    resume_len=len(resume)
    
    for i in range(resume_len):
        resume[i]=resume[i]
    
    ListOfHeading=[]
    for i in headings:                                                         #Load headings into list
        ListOfHeading.append(i)

    keys=[]
    dic={}

    for i in range(resume_len):                                                #Find headings in resume
        for j in headings:
            words=re.findall(r'[A-Za-z0-9-:()&.@/, \t |]+[A-Za-z0-9-:()&.@/,\t |]',resume[i])
            if len(words)!=0:
                if j == words[0].lower():
                    keys.append([words[0],i])
    key_length=len(keys)
    
    for k in range(key_length-1):                                              #Make a dictionary of data  with the help of corresponding heading
        dic[keys[k][0].lower()]=resume[keys[k][1]+1:keys[k+1][1]]
        
    dic['about']=resume[:keys[0][1]],resume[keys[key_length-1][1]:]            #Extra data goes into "About" heading 
   
    return dic
  
def experience(filename):                                                     # Main Function - Resume Parser Calls from this function
    dic=parser(filename)
    
    df = pd.read_excel('Heading of Experience Related Words.xlsx')            # Load Experience Heading Dataset
    headings=df.iloc[:,0]
    headings=list(headings)
    resume_heading=dic.keys()
    
    for i in headings:                                                        # Search Experience word related heading in resume
        if i in resume_heading:
            return dic[i]
            break