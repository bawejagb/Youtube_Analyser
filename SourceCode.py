import time
import httplib2
import os
import sys
import csv
from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

timer=0.001
count=0

fresult= {"positivenum":0,"negativenum":0,"neutralnum":0,"linknum":0}

commentbot = SentimentIntensityAnalyzer()

CLIENT_SECRETS_FILE = "client_secrets.json"

YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
        message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    with open("youtube-v3-discoverydocument.json", "r", encoding='utf-8') as f:
        doc = f.read()
        return build_from_document(doc, http=credentials.authorize(httplib2.Http()))

def get_comment_threads(youtube, video_id, comments=[], token=""):
    results = youtube.commentThreads().list(
        part="snippet",
        pageToken=token,
        videoId=video_id,
        textFormat="plainText"
    ).execute()

    for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        comments.append(text)

    if "nextPageToken" in results:
        return get_comment_threads(youtube, video_id, comments, results["nextPageToken"])
    else:
        return comments

def ValidatingVideoID(v_link):
    if("watch?v=" in v_link):
         return v_link.split("watch?v=")[1]
    print("\nISSUE in Link: ", v_link, "\n")
    exit(0)

if __name__ == "__main__":
  #video_id = "y3tTOePEIV4"
  video_link = "https://www.youtube.com/watch?v=WJ-UaAaumNA"
  video_id = ValidatingVideoID(video_link)
  print("\nVideo ID: ", video_id)
  args = argparser.parse_args()
  args.videoid = video_id
  print("Processing...")
  youtube = get_authenticated_service(args)
  try:
    video_comment_threads = get_comment_threads(youtube, args.videoid)
    with open('commentscraperfile.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for comment in video_comment_threads:
            writer.writerow([comment])
            writer.writerow("!@#$%U^&*()")

    print("\n")

    gen = ' ********************* YOUTUBE COMMENT ANALYZER *********************'
    for i in gen:
        print (i, end='')
        sys.stdout.flush()
        time.sleep(0.001)
    print("\n")

    gen= ' ********************************************************************'
    for i in gen:
        print(i, end='')
        sys.stdout.flush()
        time.sleep(0.001)

    time.sleep(timer)
    print("\n\n ==> Scraping {0} comments to commentscraperfile.csv \n".format(len(video_comment_threads)))

  except HttpError as e:
    print(" ==>An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
Positive_list = []
Negative_list = []
Neutral_list = []
Links_list = []
with open("commentscraperfile.csv","r",errors='ignore', encoding='utf-8') as csvfile:
    for line in csvfile.read().split("\n!,@,#,$,%,U,^,&,*,(,)\n"):
        vs = commentbot.polarity_scores(line)
        if(count == len(video_comment_threads)):
            break
        count += 1
        if("https" in line):
            Links_list.append(line)
            fresult["linknum"] +=1
        elif("http" in line):
            Links_list.append(line)
            fresult["linknum"] +=1
        elif vs['compound']>= 0.05:
            Positive_list.append(line)
            fresult["positivenum"] +=1
        elif vs['compound']<= - 0.05:
            Negative_list.append(line)
            fresult["negativenum"] += 1
        else:
            Neutral_list.append(line)
            fresult["neutralnum"] += 1

print("\n")

gen = ' ************************ GENERATING REPORT *************************'
for i in gen:
    print(i, end='')
    sys.stdout.flush()
    time.sleep(0.001)
print("\n")
time.sleep(0.001)
print("\n ==> READING THROUGH A TOTAL OF",count,"LINES...\n")

time.sleep(0.001)
print(" ==> AFTER ANALYZING THE SENTIMENT OF",count,"LINES..\n")

positivenum = fresult["positivenum"]
time.sleep(0.001)
print(" ==> NUMBER OF POSITIVE COMMENTS ARE : ",positivenum,"\n")

negativenum = fresult["negativenum"]
time.sleep(0.001)
print(" ==> NUMBER OF NEGATIVE COMMENTS ARE : ",negativenum,"\n")

neutralnum  = fresult["neutralnum"]
time.sleep(0.001)
print(" ==> NUMBER OF NEUTRAL COMMENTS ARE : ",neutralnum,"\n")
linknum  = fresult["linknum"]
time.sleep(0.001)
print(" ==> NUMBER OF COMMENTS THAT CONTAIN LINK ARE : ",linknum,"\n")

positive_percentage = positivenum / count * 100

negative_percentage = negativenum / count * 100

neutral_percentage = neutralnum / count * 100

linknum_percentage = linknum / count * 100

size1 = positive_percentage / 100 * 360

size2 = negative_percentage / 100 * 360

size3 = neutral_percentage / 100 * 360

size4 = linknum_percentage / 100 * 360
time.sleep(0.001)
print(" ==> PERCENTAGE OF COMMENTS THAT ARE POSITIVE : ",positive_percentage,"%\n")
time.sleep(0.001)
print(" ==> PERCENTAGE OF COMMENTS THAT ARE NEGATIVE : ",negative_percentage,"%\n")
time.sleep(0.001)
print(" ==> PERCENTAGE OF COMMENTS THAT ARE NEUTRAL  : ",neutral_percentage,"%\n")
time.sleep(0.001)
print(" ==> PERCENTAGE OF COMMENTS THAT CONTAIN LINK  : ",linknum_percentage,"%\n")
time.sleep(0.001)
print(" ==> CALCULATING FINAL RESULT.. :-\n")
time.sleep(3)
print(" ********************************************************************\n")

if positive_percentage >= (neutral_percentage + negative_percentage + 10) :
    print(" ==> You got positive feedback.")

elif negative_percentage>= (neutral_percentage + positive_percentage + 10):
    print(" ==> You got negative feedback.")

else :
    print(" ==> You got neutral feedback.")


with open('Positive_comments.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for comment in Positive_list:
            writer.writerow([comment])
with open('Negative_comments.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for comment in Negative_list:
            writer.writerow([comment])
with open('Neutral_comments.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for comment in Neutral_list:
            writer.writerow([comment])
with open('Links_comments.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for comment in Links_list:
            writer.writerow([comment])
#print("\nSegragated comment write done!")

print("\n ********************************************************************\n")

labels = 'Positive', 'Negative ','Neutral', 'Links'

sizes = [size1, size2, size3, size4]

colors = ['Green', 'Red', 'gold', 'blue']

explode = (0.01, 0.01, 0.01, 0.01)

patches, texts = plt.pie(sizes, explode=explode, colors=colors
,startangle=120)

plt.legend(patches, labels, loc="best")

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%',startangle= 120, textprops={'fontsize': 10})

plt.tight_layout()

plt.axis('equal')

plt.show()
