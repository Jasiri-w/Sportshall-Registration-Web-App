from django.shortcuts import render
from django.conf import settings

from .models import Student, EventTemplate, EventInstance, Registration, Schedule  
from django.contrib.auth.models import User

from .updates import *

import datetime
from json import dumps, loads

from django.core.files.storage import FileSystemStorage

def dictify(object_arg, key):
    newDict= {}

    for el in object_arg:
        newDict[el.key] = el.__dict__
        newDict[el.key]['_state'] = None

    return newDict


# Create your views here.
def dummyView(request, *args, **kwargs):
    pass

def signUp(request, *args, **kwargs):
    newRegistration = Registration(
        registration_date = datetime.datetime.now(),
        event_id_id = request.POST['eventID'],
        user_id_id = request.POST['userID'],
    )
    newRegistration.save()

    context = {
        "Students" : [student for student in Student.objects.all()],
        "Events" : [event for event in EventInstance.objects.all()],
        "Registrations" : [reg for reg in Registration.objects.all()],
    }
    return render(request, 'frontend/home.html', context)

def sheetView(request, event_id_id_id, *args, **kwargs):
    #print("\n\nSheet view logic running")

    RegQuery = f"SELECT registration_id, event_name, event_date, schedule_id, template_id, student_id, first_name, last_name, id, session, day, student_first_name, student_last_name, altFrontend_student.gender AS student_gender, altFrontend_student.year_group AS year_group, boarding_house, altFrontend_student.user_id_id FROM altFrontend_registration JOIN altFrontend_eventinstance ON event_id = event_id_id JOIN altFrontend_schedule ON schedule_id_id = schedule_id JOIN altFrontend_eventtemplate ON template_id = template_id_id JOIN auth_user ON auth_user.id = altFrontend_registration.user_id_id JOIN altFrontend_student ON altFrontend_student.user_id_id = altFrontend_registration.user_id_id WHERE event_id = { event_id_id_id };"
    StudentQuery = f"SELECT * FROM altFrontend_student WHERE gender =  '{EventTemplate.objects.get(template_id = Schedule.objects.get(schedule_id = EventInstance.objects.get(event_id = event_id_id_id).schedule_id_id).template_id_id).gender }' AND year_group =  '{EventTemplate.objects.get(template_id = Schedule.objects.get(schedule_id = EventInstance.objects.get(event_id = event_id_id_id).schedule_id_id).template_id_id).year_group }' "
    EventQuery = f"SELECT event_id, event_date, session, day, event_name, gender, maximum_capacity, year_group  FROM altFrontend_eventinstance JOIN altFrontend_schedule ON schedule_id = schedule_id_id JOIN altFrontend_eventtemplate ON template_id = template_id_id WHERE event_id = { event_id_id_id };"
    students = {}
    for el in Student.objects.raw(str(StudentQuery)):
        #print("El: ", el)
        students[el.student_id] = el.__dict__
        students[el.student_id]['_state'] = None
        #print("students[el.students_id] ", students[el.student_id])
    registered = {}
    for el in Registration.objects.raw(str(RegQuery)):
        registered[el.student_id] = el.__dict__
        registered[el.student_id]['_state'] = None

    context = {
        "Event" : EventInstance.objects.raw(EventQuery)[0].__dict__,
        "Students" : students,
        "Registered" : registered
    }
    context["Event"]['_state'] = None
    context["Event"]['event_date'] = context["Event"]['event_date'].strftime("%x")
    context["JSON"] = dumps(context, default=str)

    return render(request, 'frontend/sheet.html', context)

##########################################################################################################################################

def homeView(request, *args, **kwargs):
    
    updateInstanceModel()

    # All the values/parameters/variables passed to the html through Django's rendering function: a dict of data passed to the frontend
    context = {}

    # Upcoming events such as tonights basketball or tommorrow mornings squash
    upcomingevents = []
    equery = f"select event_id, schedule_id_id, session, day, template_id, event_name, gender, year_group, maximum_capacity from altFrontend_eventinstance join altFrontend_schedule on altFrontend_schedule.schedule_id = altFrontend_eventinstance.schedule_id_id join altFrontend_eventtemplate on altFrontend_eventtemplate.template_id = altFrontend_schedule.template_id_id where gender = '{ Student.objects.get(user_id_id = request.user.id).gender }' and year_group = { Student.objects.get(user_id_id = request.user.id).year_group } ;" if request.user != None and Student.objects.filter(user_id_id = request.user.id).exists() else "select event_id, schedule_id_id, session, day, template_id, event_name, gender, year_group, maximum_capacity from altFrontend_eventinstance join altFrontend_schedule on altFrontend_schedule.schedule_id = altFrontend_eventinstance.schedule_id_id join altFrontend_eventtemplate on altFrontend_eventtemplate.template_id = altFrontend_schedule.template_id_id;"
    querySet = EventInstance.objects.raw(equery)
    for event in querySet :
        #print(event.event_date.day - datetime.datetime.now().day)
        if event.event_date.day - datetime.datetime.now().day <= 1:
            upcomingevents.append(event)

    # Queries the Registration table for the current users registrations: all the events the user is signed up for 
    userEvents = {}
    if not request.user.id == None:
        userEventsQuery = f"SELECT registration_id, event_id_id, registration_date, student_first_name, student_last_name, boarding_house, year_group, gender, altFrontend_student.user_id_id FROM altFrontend_registration JOIN auth_user ON id = altFrontend_registration.user_id_id JOIN altFrontend_student ON altFrontend_student.user_id_id = id WHERE altFrontend_student.user_id_id = { request.user.id };"
        userEventsQuerySet = Registration.objects.raw(userEventsQuery)
        for event in userEventsQuerySet:
            userEvents[event.registration_id] = event.__dict__
            userEvents[event.registration_id]["_state"] = None
    
    # When the user clicks sign up or any other request/form submission is sent from "home.html" 
    if  request.method == 'POST':
        # Checks to see if a Registration table entry already exists with both the specific event ( which changes every new time the event comes) and linked to the user
        if not Registration.objects.filter(event_id = request.POST['eventID']).filter(user_id = request.POST['userID']).exists():
            vent = EventInstance.objects.get(event_id = request.POST['eventID'])
            newRegistration = Registration(
                registration_date = datetime.datetime.now(),
                event_id_id = vent.event_id,
                user_id_id = request.POST['userID'],
            )
            newRegistration.save()
        else:
            # If the user is already registered write this at the top of the page
            context["Message"] = "<span style='color: red;'><em>You are already signed up for this activity<em></span>"

    context = {
        #"Students" : [student for student in Student.objects.all()], Until we decide wether we want to show whos signed up for what
        #"Registrations" : [reg for reg in Registration.objects.all()],
        "UpcomingEvents" : upcomingevents,
        "UserEvents" : userEvents,
        "UpcomingEventsDict" : {},
        "AllEvents" : EventTemplate.objects.all()
    }

    # In order for these elements to be JSONifiable they must be converted to dicts
    for event in upcomingevents:
        context["UpcomingEventsDict"][event.event_id] = event.__dict__
        context["UpcomingEventsDict"][event.event_id]["_state"] = None

    context["JSON"] = dumps(context, default=str)

    return render(request, 'frontend/home.html', context)

def addEventToSchedule(request, *args, **kwargs ):

    newScheduleElement = Schedule(
        event_name= request.POST['eventname'],
        gender = request.POST['gender'],

        session = request.POST['session'],
        day = datetime.datetime.now().strftime("%A"),
        template_id_id = request.POST['template_id']
    )
    newScheduleElement.save()
    context ={}
    return render(request, 'frontend/home.html', context )

#####################################################################

def scheduleView(request, *args, **kwargs ):
    

    
    eventTemplates = {}
    for event in EventTemplate.objects.all():
        eventTemplates[event.template_id] = event.__dict__
        eventTemplates[event.template_id]['_state'] = None
    eventInstances = {}
    for event in EventInstance.objects.all():
        eventInstances[event.event_id] = event.__dict__
        eventInstances[event.event_id]['_state'] = None
    registrations = {}
    for reg in Registration.objects.all():
        registrations[reg.registration_id] = reg.__dict__
        registrations[reg.registration_id]['_state'] = None

    context = {}
    database_data = {
        "EventTemplates" : eventTemplates,
        "EventInstances" : eventInstances,
        "Registrations" : registrations,
    }

    
    if request.method == 'POST':
        if len(request.FILES) > 0:
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            new_document = fs.save(uploaded_file.name, uploaded_file)
            context['file_url'] = fs.url(new_document)

        elif request.POST['tableData'] != 1:
            '''print("New POST malone drop")

            request.POST['tableData']

            newStudent = Student(
                user_id_id = request.POST['userID'],

            )
            newStudent.save()'''
            #print(str(request.POST['tableData']))
            '''quote_count = 0
            str_list = list(request.POST['tableData'])
            for charIndex in range(len(request.POST['tableData'])):
                if(str_list[charIndex] == '"'):
                    quote_count += 1
                    if(str_list[charIndex+1] == ' '):
                        str_list.insert(charIndex+1, ",")
            
            final_string = ''.join(str_list)
            print(loads(final_string))'''
            Schedule.objects.all().delete()
            raw_table_data = loads(request.POST['tableData'])
            for event in raw_table_data:
                newSchedule = Schedule(
                    session = raw_table_data[event]["session"],
                    day = raw_table_data[event]["day"],
                    template_id_id = raw_table_data[event]["templateID"],
                )
                newSchedule.save()

            updateInstanceModel()

    schedule = {}
    for event in Schedule.objects.all():
        schedule[event.schedule_id] = event.__dict__
        schedule[event.schedule_id]['_state'] = None
    database_data['Schedule'] = schedule 
    context['JSON'] = dumps(database_data, default=str)
    print("Hello?")
    print(context['JSON'])
    return render(request, 'frontend/schedule.html', context)

def editScheduleView(request, *args, **kwargs ):

    
    context= {
        "ScheduleElements" : EventTemplate.objects.all()
    }
    
    return render(request, 'frontend/schedule_edit.html', context )

#####################################################################

def studentDetailsView(request, *args, **kwargs):
    genders = []
    for g in range(len(Student.GENDERS)):
        genders.append(Student.GENDERS[g][1])
    
    boardinghouses = []
    for b in range(len(Student.BOARDINGHOUSES)):
        boardinghouses.append(Student.BOARDINGHOUSES[b][1])
    
    yeargroups = []
    for year in Student.YEARGROUPS:
        yeargroups.append(year.value)

    context = {
        "Genders" : genders,
        "BoardingHouses" : boardinghouses,
        "YearGroups" : yeargroups
    }

    return render(request, 'frontend/create/student.html', context)

def newStudent(request, *args, **kwargs):
    if not Student.objects.filter(user_id = request.POST['userID']).exists():
        newStudent = Student(
            user_id_id = request.POST['userID'],
            student_first_name = request.POST['firstname'],
            student_last_name = request.POST['lastname'],
            boarding_house = request.POST['bhouse'],
            year_group = request.POST['yeargroup'],
            gender = request.POST['gender']
        )
        newStudent.save()
        context = {
            "Valid" : True,
            "Message": "Succesfully created your account"
        }
        return render(request, 'frontend/create/student.html', context)
    else:
        Student.objects.filter(user_id = request.POST['userID']).update(
            user_id = request.POST['userID'],
            student_first_name = request.POST['firstname'],
            student_last_name = request.POST['lastname'],
            boarding_house = request.POST['bhouse'],
            year_group = request.POST['yeargroup'],
            gender = request.POST['gender']
        )
        context = {
            "Valid" : True,
            "Message": "Sucessfully updated your details"
        }
        return render(request, 'frontend/create/student.html', context)

#####################################################################

def createEventView(request, *args, **kwargs):
    genders = []
    for g in range(len(Student.GENDERS)):
        genders.append(Student.GENDERS[g][1])

    yeargroups = []
    for year in Student.YEARGROUPS:
        yeargroups.append(year.value)
    
    context = {
        "YearGroups" : yeargroups,
        "Genders" : genders,
        "Schedule" : [ event for event in Schedule.objects.all()],
        "AllEventTemplates" : EventTemplate.objects.all(),
        "Valid" : True,
        "Message" : "",
    }

    return render(request, 'frontend/create/event.html', context)

def newEvent(request, *args, **kwargs):
    
    events = []
    for event in EventInstance.objects.all():
        if event.event_date == datetime.datetime.now():
            events.append(event.event_name)

    context = {
        "Valid" :   False,
        "Message" : "Already Exists"
    }

    if request.POST['eventname'] not in events:
        
        newEventTemplate = EventTemplate(
            event_name = request.POST['eventname'],
            gender = request.POST['gender'],
            year_group = request.POST['yeargroup'],
            maximum_capacity = request.POST['maxcap'],
        )
        newEventTemplate.save()
        context = {
            "Valid" :   True,
            "Message" : "",
        }


    return render(request, 'frontend/create/event.html', context)

#####################################################################

def addName(request, *artgs,**kwargs):
    '''newStudent = Student(student_first_name="Jasiri", student_last_name="Mumina Wa-Kyendo",boarding_house = "TS", year_group=12, gender="Male")
    newStudent.save'''
    return render(request, 'frontend/sheet.html')
