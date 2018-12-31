# fantt
Field Audio Notes Transcriber and Timestamper

Welcome to Field Audio Notes Transcriber and Timestamper.
The purpose is to take pre-recorded audio notes and
produce a simple .csv file with timestamps and the spoken phrases
using IBMs Watson AI.

The output .csv will look like this:
   0
   1.29	2.69	I'm a lumberjack
   3.7	4.96	and that' ok

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
   OK, You need to have a key file for Watson here.  and you need a LITE account
   LITE is good for 100 minutes per month.
   goto https://cloud.ibm.com/registration?target=%2Fapidocs
   You will enter a username and pw
   Off to your email, confirm the account.  They ask for your IBMid it's your username
   Now, Create Resource in upper right. Scroll to find Speech to Text.  You only get one resource.
   Select that, and then in lower right, Create
   Follow directions, go to Dashboard, manage page, click show to view your credentials
   Click Manage; Security, Platform API keys, Create.  Name the key, not YOUR name
   Paste that key into a file which must be in this folder with name Fantt_Readme_Support.txt

I'll create a file like this one, in your working directory
Change what you want, except it must have at least three lines with first four 
letters each exactly KEY= URL= CTR= e.g.

KEY=<yourkeyhere>
URL=https://stream.watsonplatform.net/speech-to-text/api
CTR=2
  
The initial URL provided is for Dallas, TX, USA.
There are better choices internationally, please check Watson's site.
While we're setting up. You must also, from your own cli,  

pip install watson_developer_cloud
or
pip3 install watson_developer_cloud
