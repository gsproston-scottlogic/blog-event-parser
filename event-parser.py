import datetime
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

def writeEventToFile(event): 
  # create title
  pass

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
    writeEventToFile(event)

exit(0)