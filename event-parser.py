import codecs
import datetime
import os
import re
import sys
import xml.etree.ElementTree as et

from event import Event

def parseEventXml(inputFile):
  # list of events
  events = []

  # parse input file
  tree = et.parse(inputFile)
  root = tree.getroot()
  for item in root.findall("./channel/item"):
    # parse out text elements
    title = item.find("title").text
    link = item.find("link").text
    guid = item.find("guid").text

    # parse out datetimes
    eventDateStr = item.find("events_date").text
    eventDateFormat = "%Y%m%d"
    eventDate = datetime.datetime.strptime(eventDateStr, eventDateFormat)
    pubDateTimeStr = item.find("pubDate").text
    pubDateTimeFormat = "%a, %d %b %Y %H:%M:%S %z"
    pubDateTime = datetime.datetime.strptime(pubDateTimeStr, pubDateTimeFormat)

    # get all the speakers
    speakers = []
    for speaker in item.findall("event_speaker/ul/li"): 
      if (speaker != None and speaker.text != None):
        speakers.append(speaker.text)

    # parse out the description
    description = item.find("description").text
    # remove start and end tags
    description = description.replace("<![CDATA[", "")
    description = description.replace("]]>", "")
    # remove leading and trailing whitespace
    description = description.strip()

    # create event object
    event = Event(title, link, pubDateTime, guid, speakers, eventDate, description)
    events.append(event)

  # return the list of events
  return events

def writeEventToFile(event: Event, outputDir): 
  # create file name from event date and title
  fileName = event.title
  # convert to lowercase
  fileName = str.lower(fileName)
  # remove symbols from the title
  fileName = re.sub(r'[^\w ]', '', fileName)
  # replace spaces with dashes
  fileName = fileName.replace(" ", "-")
  # prepend with the date
  fileName = event.eventDate.strftime("%Y-%m-%d-") + fileName
  # add the 'md' extension
  fileName = fileName + ".md"

  # open file for writing
  pathToFile = os.path.join(outputDir, fileName)
  f = open(pathToFile, "w", encoding="utf-8")
  # header
  f.write("---")
  f.write("\ntitle: " + event.title)
  f.write("\nlink: " + event.link)
  f.write("\nguid: " + event.guid)
  f.write("\neventDate: " + event.eventDate.strftime("%Y-%m-%d"))
  f.write("\npubDateTime: " + event.pubDateTime.strftime("%Y-%m-%d %H:%M:%S %z"))
  # speakers
  if (len(event.speakers) > 0):
    f.write("\nspeakers:")
    for speaker in event.speakers: 
      f.write("\n\t- ")
      f.write(speaker)
  f.write("\n---\n\n")
  # body
  f.write(event.description)
  # done writing
  f.close()

if __name__ == "__main__": 
  # must have two arguments
  if (len(sys.argv) < 3):
    print("Must be given two arguments")
    exit(1)

  # get the input file and output directory
  inputFile = sys.argv[1]
  outputDir = sys.argv[2]

  print("Input file: " + inputFile)
  print("Output directory: " + outputDir)

  events = parseEventXml(inputFile)
  for event in events:
    writeEventToFile(event, outputDir)

exit(0)