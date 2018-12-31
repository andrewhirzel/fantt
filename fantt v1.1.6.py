from __future__ import print_function
#!/usr/bin/python
#this is in python 2.7 + and 3.6+

fantt_version = "1.1.6"

# Field Audio Notes Transcriber & Timestamper
#December 31, 2018
#Andrew Hirzel ahirzel@protonmail.com

#following imports should be installed with pip (or pip3) 
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud import WatsonApiException

from os.path import join, dirname, splitext, exists, getsize
import sys

#this file is where we look for the key, in your current folder
#if it is not existing we'll create it
FANTT_API_FILE = "Fantt_Readme_Support.txt"

#change if you have preference to the output.  An csv wil be created in
# the current folder
#I would leave it as .csv, makes easier to open in a spreadsheet tool
FILE_PAD = "_fantt.csv"

ENUM_LIST = { 1 : 'first', 2 : 'second', 3 : 'third', 4 : 'final' }

def Make_Api_File(key,url,counter) :
        
   try:
        wf = open(FANTT_API_FILE,"w")
        wf.write ('Welcome to Field Audio Notes Transcriber and Timestamper v' + fantt_version+'\n')
        wf.write ('The purpose is to take pre-recorded audio notes and \n')
        wf.write ('produce a simple .csv file with timestamps and the spoken phrases\n')
        wf.write ('using IBMs Watson AI.\n')
        wf.write ('Note:\n')
        wf.write ('1. Your data will not at all be considered private.\n')
        wf.write ('2. File size not less than 100B, not larger than 100MB\n')
        wf.write ('3. Existing, in this folder, expecting one or more audio files\n')
        wf.write ('4. Enter the files in the order you want them processed\n')
        wf.write ('5. Must all be of the same type and please do include the extensions\n')
        wf.write ('6. Enter a blank enter-key when no more files\n')
        wf.write ('7. Will be overwriting the results into the first file name\n')
        wf.write ("\n")
        wf.write ("\n")
        wf.write ("This is how you obtain the Watson API key file, for Fantt\n")
        wf.write ("OK, You need to have a key file for Watson here.  and you need a LITE account\n")
        wf.write ("LITE is good for 100 minutes per month.\n")
        wf.write ("goto https://cloud.ibm.com/registration?target=%2Fapidocs\n")
        wf.write ("You will enter a username and pw\n")
        wf.write ("Off to your email, confirm the account.  They ask for your IBMid it's your username\n")
        wf.write ("Now, Create Resource in upper right. Scroll to find Speech to Text.  You only get one resource.\n")
        wf.write ("Select that, and then in lower right, Create\n")
        wf.write ("Follow directions, go to Dashboard, manage page, click show to view your credentials\n")
        wf.write ("Click Manage; Security, Platform API keys, Create.  Name the key, not YOUR name\n")
        wf.write ("Paste that key into a file which must be in this folder with name " +FANTT_API_FILE+"\n")
        wf.write ("This file we re in can be shorter, but it must have at least two lines with first four \n")
        wf.write ("letters each exactly KEY= and URL= e.g.\n")
        wf.write ("\n")
        wf.write ("KEY="+key+"\n")
        wf.write ("URL="+url+"\n")
        wf.write ("\n")
        wf.write ("The initial URL provided is for Dallas, TX, USA.\n")
        wf.write ("There are better choices internationally, please check Watson's site.\n")
        wf.write ("While we're setting up. You must also, from your cli,  \n")
        wf.write ("pip install watson_developer_cloud\n")
        wf.write ("Or maybe pip3 depending your install of python\n")
        wf.write ("CTR="+str(counter)+"\n")
        wf.close()

   except IOError as e:
        print ("Forced Error, must be able to create a local file"+ Error({0}))

   return

#all of the real work is done here
def worker(Speech_Files,KEY,URL) :
  
    try:
        speech_to_text = SpeechToTextV1(iam_apikey=KEY,url=URL)
    except WatsonApiException as ex:
        print ("Forced Exit, Watson Error, " + str(ex.code) + ": " + ex.message)
        return
    
    #create the output file only if warranted with real input, so check
    if not exists(Speech_Files[0]):
        print ("Forced exit, Cannot read your first filename: " + Speech_Files[0])
        return

    #output name is base without extension + fantt
    try :
            Fixed_Output = open(splitext(Speech_Files[0])[0]+FILE_PAD,"w")
            Fixed_Output.write ("0.00\n")

            # find the file type extension, without the period
            AUDIOTYPE = 'audio/'+ splitext(Speech_Files[0])[1][1:]

            #this adds from one file's endstamp to the next files startstamp
            lasttime = 0

            for file in Speech_Files:
              if not exists(file):
                print ("Forced exit, Cannot read your filename: " + file)
                return
              else :
                #provide user with some updates
                seconds = int(((getsize(file)) / 30000 +10) / 10)*10

                if seconds > 10 :print ('Guessing it will take '+str(seconds)+'-'+str(seconds+5)+
                       ' seconds to process '+file)
                else : print("Guessing it will be only a few seconds")
                
                try:
                  with open(join(dirname(__file__), './.', file),
                               'rb') as audio_file:
                      speech_recognition_results = speech_to_text.recognize(
                        audio=audio_file,
                        content_type=AUDIOTYPE,
                        timestamps=True,
                        word_alternatives_threshold=0.9
                      ).get_result()


                      for FullSpeech in speech_recognition_results["results"] :
                        for Option in FullSpeech :
                            if Option == "alternatives" : 
                                  for SpeechDetail in FullSpeech[Option] :
                                      for PhraseDetail in SpeechDetail :
                                          if PhraseDetail == "timestamps" :
                                              PhraseLength = len(SpeechDetail[PhraseDetail])
                                              wordcount = 0
                                              for Word in SpeechDetail[PhraseDetail] :
                                                  if wordcount == 0 :
                                                      Fixed_Output.write(str(Word[1]+lasttime)+",")
                                                      print (str(Word[1]+lasttime)," ",end="")
                                                  if wordcount == PhraseLength - 1 :
                                                      Fixed_Output.write(str(Word[2]+lasttime)+",")
                                                      print (str(Word[2]+lasttime)," ",end="")
                                                      newlasttime = Word[2]
                                                  wordcount += 1
                                          
                                          if PhraseDetail == "transcript" :
                                              Fixed_Output.write(SpeechDetail[PhraseDetail]+ "\n")
                                              print (SpeechDetail[PhraseDetail])
                                                  
                      lasttime = newlasttime
                except WatsonApiException as ex:
                    print ("Forced Exit, Watson Error, " + str(ex.code) + ": " + ex.message)

            Fixed_Output.close()
    except :
        print ("Forced Error, cannot create your output file"+ Error({0}))

    return

def main():

    #get the key and URL
    if not exists(FANTT_API_FILE):

        print ("you did not have a Fantt Setup file.  Will try to create one, please read it")
        Make_Api_File("falsekey","https://stream.watsonplatform.net/speech-to-text/api",0)
        return

    with open(FANTT_API_FILE) as f:
        mylist = f.read().splitlines() 

    key = "a"
    url = "a"
    #default to one more verbose
    ctr = str(len(ENUM_LIST)-1)
    
    for sline in mylist :
        if sline[:4]=="KEY=" : key = sline[4:]
        if sline[:4]=="URL=" : url = sline[4:]
        if sline[:4]=="CTR=" : ctr = sline[4:]
    
    #at least make sure something was found
    if len(key) < 10  :
        print ("Forced Exit, Watson KEY not right, I have: "+ key)
        return

    if len(url) < 10  :
        print ("Forced Exit, Watson URL not right, I have: "+ url )
        return
    
    print ('Welcome to Field Audio Notes Transcriber and Timestamper v' + fantt_version)

    try :
       counter = int(ctr)
    except :
       counter = len(ENUM_LIST)-1
       
    if counter < len(ENUM_LIST)   :
        print ('The purpose is to take pre-recorded audio notes and ')
        print ('produce a simple .csv file with timestamps and the spoken phrases')
        print ('using IBMs Watson AI.')
        print ('Notes:')
        print ('1. Your data will not at all be considered private.')
        print ('2. File size not less than 100B, not larger than 100MB')
        print ('3. Existing, in this folder, expecting one or more audio files')
        print ('4. Enter the files in the order you want them processed')
        print ('5. Must all be of the same type and please do include the extensions')
        print ('6. Enter a blank enter-key when no more files')
        print ('7. Will be overwriting the results into the first file name + ' + FILE_PAD)
        print ("This is the "+str(ENUM_LIST[counter+1])," of "+str(len(ENUM_LIST))," times you're forced to see this high level of verbosity\n")

        Make_Api_File(key,url,counter+1)
                
    #get the files from the user
    #in future, maybe just take all the files in a fixed directory?
    fileset = []
    s = "a"
    fcounter = 1
    while len(s) > 0 :
        requestphrase = "enter name of file #" + str(fcounter) + " "
        if sys.version_info[0] > 2 : s = input(requestphrase)
        else : s = raw_input(requestphrase)
        if len(s) > 0 : fileset.append(s)
        fcounter += 1
        
    if counter < len(ENUM_LIST)   :
            print ("Hmm, this could take a few minutes, i.e. a 3MB file might take a minute or more.")
            print ("You realize, need to upload the files, depends on your connection")
            print ("Then using Watson to sift through and consider your audio")
            print ("So cannot provide much in the way of interim results")
            print ('No swirly hourglass or nodding daisy.')
    print ('Be patient.') 

    worker(fileset,key,url)

if __name__ == "__main__":
    main()
