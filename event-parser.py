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
    title = item.find("title").text
    link = item.find("link").text
    pubDate = item.find("pubDate").text
    guid = item.find("guid").text
    eventDate = item.find("events_date").text

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
    event = Event(title, link, pubDate, guid, speakers, eventDate, description)
    events.append(event)

  # return the list of events
  return events

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

exit(0)