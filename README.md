
# fantt
Field Audio Notes Transcriber and Timestamper

Welcome to Field Audio Notes Transcriber and Timestamper.
The purpose is to take pre-recorded audio notes and
produce a simple .csv file with timestamps and the spoken phrases
using IBMs Watson AI.  To get you interested, here's your sample output.


   0   
   1.29	2.69	I'm a lumberjack   
   3.7	4.96	and that's ok

Notes:
   1. Your data will not at all be considered private.  This is IBM's warning AND mine.
   2. File size not less than 100B, not larger than 100MB, again IBM's rule.
   3. Existing, in this folder, I'm expecting one or more audio files
   4. Enter the files in the order you want them processed, and I'll append them together
      i.e files Spam.mp3, Eggs.mp3, Ham.mp3 will end up in Spam_fantt.csv
   5. Must all be of the same type and please do include the extensions
   6. Enter a blank enter-key when no more files to process
   7. I'll be overwriting the results into the first file name

This is how you obtain the Watson API key file, for Fantt
1. OK, You need to have a key file for Watson here.  and you need a LITE account.  
2. LITE is good for 100 minutes per month.
3. Now goto https://cloud.ibm.com/registration?target=%2Fapidocs
4. You will enter a username and pw.
5. Head off to your email, confirm the account.  They ask for your IBMid (yes it's your username). 
6. Now, Create Resource in upper right. Scroll to find Speech to Text.  You only get one resource.
7. Select that, and then in lower right, Create. 
8. Follow directions, go to Dashboard, manage page, click show to view your credentials.
9.Click Manage; Security, Platform API keys, Create.  Name the key, not YOUR name.
10. Paste that key into a "Fantt_readme_support.txt" file which must be in your working folder. If it's missing, I create it.

I'll create the file like this one, in your working directory.  
Change what you want in that file, except it must have at least three lines with first four 
letters each exactly KEY= URL= CTR= e.g.

KEY='yourkeyhere'

URL=https://stream.watsonplatform.net/speech-to-text/api

CTR=2
  
The initial URL provided is for Dallas, TX, USA.
There are better choices internationally, please check Watson's site.
While we're setting up. You must also, from your own cli,  

pip install watson_developer_cloud or pip3 install watson_developer_cloud
