#!/usr/bin/python
import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import timedelta

import os

def getTotalTimeFromExportForTasksContaining(path, searchTerms):
    taskTotalTime = timedelta()
    for filename in os.listdir(path):
        if not filename.endswith('.xml'): continue
        fullname = os.path.join(path, filename)

        tree = ET.parse(fullname)
        root = tree.getroot()
        tasks = root.findall('.//Task')
        for task in tasks:
            matches = False
            for term in searchTerms:
                if term in task.attrib['Name']:
                    matches = True
                    break
            if matches:
                print(task.attrib['Name'])
                timelines = task.findall('.//TimeLine')
                taskTime = timedelta()
                for timeline in timelines:
                    closed = timeline.find('Closed').text == 'True'
                    if closed:
                        start = datetime.strptime(timeline.attrib['Start'], '%d-%m-%Y %H:%M:%S')
                        stop = datetime.strptime(timeline.find('Stop').text, '%d-%m-%Y %H:%M:%S')
                        delta = stop - start
                        taskTime += delta
                if (taskTime.seconds > 0):
                    taskTotalTime += taskTime
        return taskTotalTime

if __name__ == '__main__':
    print(getTotalTimeFromExportForTasksContaining('.', ['card','Card']))
