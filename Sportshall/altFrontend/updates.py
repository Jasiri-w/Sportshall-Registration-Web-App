from .models import EventInstance, EventTemplate, Schedule
from datetime import datetime, timedelta

def nextDay(date, day):
    days_ahead = day - date.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return date + timedelta(days_ahead)

def updateInstanceModel():
    TemplateObjects = EventTemplate.objects.all()
    InstanceObjects = EventInstance.objects.all()
    ScheduleObjects = Schedule.objects.all()

    dayMatrix = {
        "Monday" : 0,
        "Tuesday" : 1,
        "Wednesday" : 2,
        "Thursday" : 3,
        "Friday" : 4,
        "Saturday" : 5,
        "Sunday" : 6
    }

    # First: Delete any and all Event Instance Objects that reference non existent schedule items - in other words delete old/obsolete events 
    for event in InstanceObjects:
        if(len(ScheduleObjects.filter(schedule_id = event.schedule_id_id)) == 0):
            InstanceObjects.filter(event_id = event.event_id).delete()

    # Second: Add all Schedule objects to EventInstance
    for event in ScheduleObjects:
        print("Next " + event.day + " : ", nextDay(datetime.now(),dayMatrix[event.day]))
        if InstanceObjects.filter(schedule_id_id = event.schedule_id).exists() :
            InstanceObjects.filter(schedule_id = event.schedule_id).update(
                event_date = nextDay(datetime.now(),dayMatrix[event.day]),
            )
        else:
            newEvent = EventInstance(
                event_date = nextDay(datetime.now(),dayMatrix[event.day]),
                schedule_id_id = event.schedule_id,
            )
            newEvent.save()