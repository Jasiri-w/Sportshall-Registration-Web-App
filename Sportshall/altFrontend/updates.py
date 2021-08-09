from .models import *
from datetime import datetime, timedelta

dayMatrix = {
    "Monday" : 0,
    "Tuesday" : 1,
    "Wednesday" : 2,
    "Thursday" : 3,
    "Friday" : 4,
    "Saturday" : 5,
    "Sunday" : 6
}

def updateRecordModel():

    # Second: Delete all events before today
    # Second First: Iterate through all events occuring before today, then find and backup all registrations to the event in registrationrecords
    for event in EventInstance.objects.all():
        if(dayMatrix[Schedule.objects.get(schedule_id = EventInstance.objects.get(event_id = event.event_id).schedule_id_id).day] < datetime.now().weekday()):
            # If true then this event happened before today
            for reg in Registration.objects.all():
                if not RegistrationRecord.objects.filter(registration_id = reg.registration_id).exists() :
                    newRecord = RegistrationRecord(
                            user_id_id = reg.user_id_id,
        
                            # The specific event instance information
                            registration_id = reg.registration_id,
                            event_id = EventInstance.objects.get(event_id = reg.event_id_id),
                            event_date = EventInstance.objects.get(event_id = reg.event_id_id).event_date,
                            
                            # Registration information
                            registration_date = reg.registration_date,
                            day = Schedule.objects.get(schedule_id = EventInstance.objects.get(event_id = reg.event_id_id).schedule_id_id).day,
                            session = Schedule.objects.get(schedule_id = EventInstance.objects.get(event_id = reg.event_id_id).schedule_id_id).session,
                            
                            # The events information
                            template_id = Schedule.objects.get(schedule_id = EventInstance.objects.get(event_id = reg.event_id_id).schedule_id_id).template_id_id,
                            schedule_id = EventInstance.objects.get(event_id = reg.event_id_id).schedule_id_id,
                            event_name = EventTemplate.objects.get(template_id = Schedule.objects.get(schedule_id = EventInstance.objects.get(event_id = reg.event_id_id).schedule_id_id).template_id_id).event_name,
                            gender = EventTemplate.objects.get(template_id = Schedule.objects.get(schedule_id = EventInstance.objects.get(event_id = reg.event_id_id).schedule_id_id).template_id_id).gender,
                            year_group = EventTemplate.objects.get(template_id = Schedule.objects.get(schedule_id = EventInstance.objects.get(event_id = reg.event_id_id).schedule_id_id).template_id_id).year_group,
                            maximum_capacity = EventTemplate.objects.get(template_id = Schedule.objects.get(schedule_id = EventInstance.objects.get(event_id = reg.event_id_id).schedule_id_id).template_id_id).maximum_capacity
                    )
                    print(EventInstance.objects.get(event_id = reg.event_id_id).event_id ," - ", newRecord.event_name, " record was added to history.")
                    newRecord.save()

            # Second Second: Delete all the events occuring before today | this will cause all registrations of that event to be deleted as well
            print(EventTemplate.objects.get(template_id = Schedule.objects.get(schedule_id = EventInstance.objects.get(event_id = event.event_id).schedule_id_id).template_id_id).event_name , " event deleted")
            EventInstance.objects.get(event_id = event.event_id).delete()


def nextDay(date, day):
    days_ahead = day - date.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return date + timedelta(days_ahead)

def updateInstanceModel():
    TemplateObjects = EventTemplate.objects.all()
    InstanceObjects = EventInstance.objects.all()
    ScheduleObjects = Schedule.objects.all()
    RegistrationObjects = Registration.objects.all()
    RegistrationRecordObjects = RegistrationRecord.objects.all()
    # First: Delete any and all Event Instance Objects that reference non existent schedule items - in other words delete old/obsolete events 
    for event in InstanceObjects:
        if(len(ScheduleObjects.filter(schedule_id = event.schedule_id_id)) == 0):
            InstanceObjects.filter(event_id = event.event_id).delete()

    updateRecordModel()
    
    # Third: Add all Schedule objects to EventInstance
    for event in ScheduleObjects:
        #print("Next " + event.day + " : ", nextDay(datetime.now(),dayMatrix[event.day]))
        if InstanceObjects.filter(schedule_id_id = event.schedule_id).exists() :
            InstanceObjects.filter(schedule_id = event.schedule_id).update(
                event_date = nextDay(datetime.now(),dayMatrix[event.day]).replace(hour=6).replace(minute=0).replace(second = 0) if event.session == "Morning" else nextDay(datetime.now(),dayMatrix[event.day]).replace(hour=10).replace(minute=0).replace(second = 0),
            )
        else:
            newEvent = EventInstance(
                event_date = nextDay(datetime.now(),dayMatrix[event.day]).replace(hour=6).replace(minute=0).replace(second = 0) if event.session == "Morning" else nextDay(datetime.now(),dayMatrix[event.day]).replace(hour=10).replace(minute=0).replace(second = 0),
                schedule_id_id = event.schedule_id,
            )
            newEvent.save()
    