from django.shortcuts import render
from django.conf import settings

from .models import Student, EventTemplate, EventInstance, Registration, Schedule  
from django.contrib.auth.models import User

from .updates import *

import datetime
from json import dumps, loads

from django.core.files.storage import FileSystemStorage

# Create your views here.
def dummyView(request, *args, **kwargs):
    pass

def signUp(request, *args, **kwargs):
    newRegistration = Registration(
        registration_date = datetime.datetime.now(),
        event_id_id = request.POST['sportID'],
        user_id_id = request.POST['userID'],
    )
    newRegistration.save()

    context = {
        "Students" : [student for student in Student.objects.all()],
        "Events" : [event for event in EventInstance.objects.all()],
        "Registrations" : [reg for reg in Registration.objects.all()],
    }
    return render(request, 'frontend/home.html', context)

def sheetView(request, event_id, *args, **kwargs):
    #regset = Registration.objects.filter(sport_id = event_id)
    query = "SELECT registration_id, event_date, event_name, username, first_name  FROM altFrontend_registration JOIN altFrontend_eventnstance ON sport_id = sport_id_id JOIN auth_user ON id = user_id_id WHERE event_date LIKE '"+ datetime.datetime.now().strftime("%A") + "' and event_name LIKE '" + EventInstance.objects.get(sport_id = event_id).event_name + "';"


    '''for i in Registration.objects.all():
        for j in Student
            if event_id == i.sport_id:
                current.append(Student.objects.)'''

    context = {
        "Students" : [student for student in Student.objects.all()],
        "Event" : EventInstance.objects.get(event_id = event_id),
        "Registered" : [reg for reg in Registration.objects.raw(query)]
    }
    return render(request, 'frontend/sheet.html', context)

##########################################################################################################################################

def homeView(request, *args, **kwargs):
    #currentevents = EventInstance.objects.filter(event_date=datetime.datetime.now().strftime("%A"))
    
    updateInstanceModel()

    InstanceObjects = EventInstance.objects.all()
    TemplateObjects = EventTemplate.objects.all()
    ScheduleObjects = Schedule.objects.all()
    upcomingevents = []
    for event in InstanceObjects :
        print(event.event_date.day - datetime.datetime.now().day)
        if event.event_date.day - datetime.datetime.now().day <= 1:
            upcomingevents.append(EventTemplate.objects.get(template_id = Schedule.objects.get(schedule_id = event.schedule_id_id).template_id_id))


    context = {
        "Students" : [student for student in Student.objects.all()],
        "Registrations" : [reg for reg in Registration.objects.all()],
        "UpcomingEvents" : upcomingevents,
        "AllEvents" : EventTemplate.objects.all()
    }
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
        registrations[reg.name] = reg.__dict__
        registrations[reg.name]['_state'] = None

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
