from django.shortcuts import render, redirect
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

def signUp(request):
    status = {
        "Status" : False,
        "Message" : "",
    }
    # If the user is already signed up
    if not Registration.objects.filter(event_id = request.POST['eventID']).filter(user_id = request.user.id).exists():
        vent = EventInstance.objects.get(event_id = request.POST['eventID'])
        newRegistration = Registration(
            registration_date = datetime.datetime.now(),
            event_id_id = vent.event_id,
            user_id_id = request.user.id,
        )
        newRegistration.save()
        status["Status"] = True
        status["Message"] = "<span style='color: green;'><em>Signed-Up Succesfully!</em></span>"
    else:
        # If the user is already registered write this at the top of the page
        status["Message"] = "<span style='color: red;'><em>You are already signed up for this activity</em></span>"

    return status

def sheetView(request, event_id_id_id, *args, **kwargs):
    #print("\n\nSheet view logic running")

    context = {}
    response = {} 
    if request.method == "POST":
        # sign-up
        if request.POST["postIntent"] == "Sign-Up":
            response = signUp(request)

        # quit event
        if request.POST["postIntent"] =="Leave":
            Registration.objects.filter(event_id = request.POST['eventID']).filter(user_id = request.user.id).delete()
            response = "<span style='color: green;'><em>Succesfully left "+ str(EventTemplate.objects.get(template_id = Schedule.objects.get(eventinstance = EventInstance.objects.get(event_id = 32)).template_id_id).event_name) +"</em></span>"

        # save list and register students
        elif request.POST["postIntent"] == "Save-List":
            data = loads(request.POST["listData"])
            for reg in data:
                if("registration_id" in data[reg]):
                    print(Student.objects.get(user_id_id = data[reg]["user_id_id"]).student_first_name, " is already signed up!")
                    continue
                
                for x in Registration.objects.filter(event_id_id = request.POST["eventID"]):
                    if data[reg]["user_id_id"] == x.user_id_id:
                        print(Student.objects.get(user_id_id = data[reg]["user_id_id"]).student_first_name, " is already signed up!")
                        continue
                
                oldRegisteredUsers = [y.user_id_id for y in Registration.objects.filter(event_id_id = request.POST["eventID"])]
                             
                event = EventInstance.objects.get(event_id = request.POST['eventID'])
                newRegistration = Registration(
                    registration_date = datetime.datetime.now(),
                    event_id_id = event.event_id,
                    user_id_id = data[reg]["user_id_id"],
                )
                newRegistration.save()
                response["Message"] = "<span style='color: green;'><em>Everyone was Signed-Up Succesfully!</em></span>"
                print(Student.objects.get(user_id_id = data[reg]["user_id_id"]).student_first_name, " was registered successfully.")
            
            newRegisteredUsers = [data[z]["user_id_id"] for z in data]
            for y in Registration.objects.filter(event_id_id = request.POST["eventID"]):
                if(y.user_id_id not in newRegisteredUsers):
                    Registration.objects.filter(user_id_id = y.user_id_id).delete()
                    print(Student.objects.get(user_id_id = y.user_id_id).student_first_name, " did not survive the purge.")


    RegQuery = f'''
    SELECT
        registration_id,
        event_name,
        event_date,
        schedule_id,
        template_id,
        student_id,
        first_name,
        last_name,
        id,
        session,
        day,
        student_first_name,
        student_last_name,
        public."altFrontend_student".gender AS student_gender,
        public."altFrontend_student".year_group AS year_group,
        boarding_house,
        public."altFrontend_student".user_id_id
    FROM
        public."altFrontend_registration"
    JOIN
        public."altFrontend_eventinstance"
    ON
        event_id = event_id_id
    JOIN
        public."altFrontend_schedule"
    ON
        schedule_id_id = schedule_id
    JOIN
        public."altFrontend_eventtemplate"
    ON
        template_id = template_id_id
    JOIN
        auth_user
    ON
        auth_user.id = public."altFrontend_registration".user_id_id
    JOIN
        public."altFrontend_student"
    ON
        public."altFrontend_student".user_id_id = public."altFrontend_registration".user_id_id
    WHERE
        event_id = {event_id_id_id};
'''
    StudentQuery = f'''
    SELECT
        *
    FROM
        public."altFrontend_student"
    WHERE
        gender = '{EventTemplate.objects.get(template_id = Schedule.objects.get(schedule_id = EventInstance.objects.get(event_id = event_id_id_id).schedule_id_id).template_id_id).gender}'
        AND year_group = '{EventTemplate.objects.get(template_id = Schedule.objects.get(schedule_id = EventInstance.objects.get(event_id = event_id_id_id).schedule_id_id).template_id_id).year_group}';
'''
    EventQuery = f'''
    SELECT
        event_id,
        event_date,
        session,
        day,
        event_name,
        gender,
        maximum_capacity,
        year_group
    FROM
        public."altFrontend_eventinstance"
    JOIN
        public."altFrontend_schedule"
    ON
        schedule_id = schedule_id_id
    JOIN
        public."altFrontend_eventtemplate"
    ON
        template_id = template_id_id
    WHERE
        event_id = {event_id_id_id};
'''
    students = {}
    for el in Student.objects.raw(str(StudentQuery)):
        #print("El: ", el)
        students[el.student_id] = el.__dict__
        students[el.student_id]['_state'] = None
        #print("students[el.students_id] ", students[el.student_id])
    registered = {}
    is_registered = False
    for el in Registration.objects.raw(str(RegQuery)):
        if(el.id == request.user.id):
            is_registered = True
        registered[el.student_id] = el.__dict__
        registered[el.student_id]['_state'] = None

    context = {
        "Event" : EventInstance.objects.raw(EventQuery)[0].__dict__,
        "Students" : students,
        "Registered" : registered,
        "IsRegistered" : is_registered
    }
    context["Message"] = response["Message"] if "Message" in response else ""
    context["Event"]['_state'] = None
    context["Event"]['event_date'] = context["Event"]['event_date'].strftime("%x")
    print("\nMessage: ", context["Message"])
    context["JSON"] = dumps(context, default=str)

    return render(request, 'frontend/sheet.html', context)

##########################################################################################################################################

def homeView(request, *args, **kwargs):
    
    updateInstanceModel()

    # All the values/parameters/variables passed to the html through Django's rendering function: a dict of data passed to the frontend
    context = {}
    response = ""
    # When the user clicks sign up or any other request/form submission is sent from "home.html" 
    if  request.method == 'POST':
        if request.POST["postIntent"] =="Leave":
            Registration.objects.filter(event_id = request.POST['eventID']).filter(user_id = request.user.id).delete()
            response = "<span style='color: green;'><em>Unregistered Succesfully for "+ str(EventTemplate.objects.get(template_id = Schedule.objects.get(eventinstance = EventInstance.objects.get(event_id = request.POST['eventID'])).template_id_id).event_name) +"</em></span>"
        elif request.POST["postIntent"] == "Sign-Up":
            # Checks to see if a Registration table entry already exists with both the specific event ( which changes every new time the event comes) and linked to the user    
            if not Registration.objects.filter(event_id = request.POST['eventID']).filter(user_id = request.POST['userID']).exists():
                vent = EventInstance.objects.get(event_id = request.POST['eventID'])
                newRegistration = Registration(
                    registration_date = datetime.datetime.now(),
                    event_id_id = vent.event_id,
                    user_id_id = request.POST['userID'],
                )
                newRegistration.save()
                response = f"<span style='color: green;'><em>Registered Successfully for {str(EventTemplate.objects.get(template_id = Schedule.objects.get(eventinstance = EventInstance.objects.get(event_id = request.POST['eventID'])).template_id_id).event_name) } </em></span>"
            else:
                # If the user is already registered write this at the top of the page
                response = "<span style='color: red;'><em>You are already signed up for this activity</em></span>"

    # Upcoming events such as tonights basketball or tommorrow mornings squash
    upcomingevents = []

    genderFilter = "TRUE"
    yearGroupFilter = "TRUE"

    if request.user.is_authenticated and Student.objects.filter(user_id_id = request.user.id).exists():
        currentUser = User.objects.get(pk=request.user.pk)
        genderFilter = f"gender = '{ Student.objects.get(user_id_id = request.user.id).gender }'" if not currentUser.is_superuser else "TRUE"
        yearGroupFilter = f"year_group = { Student.objects.get(user_id_id = request.user.id).year_group }" if not currentUser.is_superuser != None else "TRUE"
    
    equery = f'''
    SELECT
        event_id,
        schedule_id_id,
        session,
        day,
        template_id,
        event_name,
        gender,
        year_group,
        maximum_capacity
    FROM
        public."altFrontend_eventinstance"
    JOIN
        public."altFrontend_schedule"
    ON
        public."altFrontend_schedule".schedule_id = public."altFrontend_eventinstance".schedule_id_id
    JOIN
        public."altFrontend_eventtemplate"
    ON
        public."altFrontend_eventtemplate".template_id = public."altFrontend_schedule".template_id_id
    WHERE
        ''' + genderFilter + '''
        AND ''' + yearGroupFilter + '''
''' if Student.objects.filter(user_id_id = request.user.id).exists() else '''
    SELECT
        event_id,
        schedule_id_id,
        session,
        day,
        template_id,
        event_name,
        gender,
        year_group,
        maximum_capacity
    FROM
        public."altFrontend_eventinstance"
    JOIN
        public."altFrontend_schedule"
    ON
        public."altFrontend_schedule".schedule_id = public."altFrontend_eventinstance".schedule_id_id
    JOIN
        public."altFrontend_eventtemplate"
    ON
        public."altFrontend_eventtemplate".template_id = public."altFrontend_schedule".template_id_id;
'''

    

    querySet = EventInstance.objects.raw(equery)
    for event in querySet :
        #print(event.event_date.day - datetime.datetime.now().day)
        if event.event_date.day - datetime.datetime.now().day <= 2:
            upcomingevents.append(event)

    # Queries the Registration table for the current users registrations: all the events the user is signed up for 
    userEvents = {}
    if request.user.id != None:
        userEventsQuery = f'SELECT registration_id, event_id_id, registration_date, student_first_name, student_last_name, boarding_house, year_group, gender, public."altFrontend_student".user_id_id FROM public."altFrontend_registration" JOIN public."auth_user" ON id = public."altFrontend_registration".user_id_id JOIN public."altFrontend_student" ON public."altFrontend_student".user_id_id = id WHERE public."altFrontend_student".user_id_id = { request.user.id };'
        userEventsQuerySet = Registration.objects.raw(userEventsQuery)
        for event in userEventsQuerySet:
            userEvents[event.registration_id] = event.__dict__
            userEvents[event.registration_id]["_state"] = None
    

    context = {
        #"Students" : [student for student in Student.objects.all()], Until we decide wether we want to show whos signed up for what
        "Registrations" : [reg.__dict__ for reg in Registration.objects.all()],
        "UpcomingEvents" : upcomingevents,
        "UserEvents" : userEvents,
        "UpcomingEventsDict" : {},
        "AllEvents" : EventTemplate.objects.all()
    }

    # In order for these elements to be JSONifiable they must be converted to dicts
    for event in upcomingevents:
        context["UpcomingEventsDict"][event.event_id] = event.__dict__
        context["UpcomingEventsDict"][event.event_id]["_state"] = None
    
    for event in context["Registrations"]:
        event["_state"] = None

    context["Message"] = response
    context["JSON"] = dumps(context, default=str)

    return render(request, 'frontend/home.html', context)

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
            "Message": "Successfully updated your details"
        }
        return render(request, 'frontend/create/student.html', context)

#####################################################################

def editEventView(request, *args, **kwargs):
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

def createEvent(request, *args, **kwargs):
    
    events = []
    for event in EventInstance.objects.all():
        if event.event_date == datetime.datetime.now():
            events.append(event.event_name)

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

        context["Valid"] = True
        context["Message"] = ""

    return render(request, 'frontend/create/event.html', context)

#####################################################################

def addName(request, *artgs,**kwargs):
    '''newStudent = Student(student_first_name="Jasiri", student_last_name="Mumina Wa-Kyendo",boarding_house = "TS", year_group=12, gender="Male")
    newStudent.save'''
    return render(request, 'frontend/sheet.html')

######################################################################

def settingsView(request, *args, **kwargs):

    genders = []
    for g in range(len(Student.GENDERS)):
        genders.append(Student.GENDERS[g][1])
    
    boardinghouses = []
    for b in range(len(Student.BOARDINGHOUSES)):
        boardinghouses.append(Student.BOARDINGHOUSES[b][1])
    
    yeargroups = []
    for year in Student.YEARGROUPS:
        yeargroups.append(year.value)

    student = Student.objects.get(user_id_id = request.user.id) if Student.objects.filter(user_id_id = request.user.id).exists() else ""
    
    context = {
        "Genders" : genders,
        "BoardingHouses" : boardinghouses,
        "YearGroups" : yeargroups,
        "student" : student,
    }

    if request.method == 'POST':
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
            context["Message"] = "Succesfully created your account"
        else:
            Student.objects.filter(user_id = request.POST['userID']).update(
                user_id = request.POST['userID'],
                student_first_name = request.POST['firstname'],
                student_last_name = request.POST['lastname'],
                boarding_house = request.POST['bhouse'],
                year_group = request.POST['yeargroup'],
                gender = request.POST['gender']
            )
            context["Message"] = "Successfully updated your details"

        currentUser = User.objects.get(pk=request.user.pk)
        currentUser.first_name = request.POST['firstname']
        currentUser.last_name = request.POST['lastname']
        currentUser.save()


    return render(request, 'frontend/settings.html', context)


######################################################################]

def getCurrentSession():
    noonTime = datetime.time(13, 0, 0)
    return "Morning" if datetime.datetime.now().time() < noonTime else "Evening"

def addEventToTodayView(request, event_id_id_id, *args, **kwargs):

    context = {}

    newScheduleEntity= Schedule(
        session = getCurrentSession(),
        day = datetime.datetime.now().strftime("%A"),
        template_id_id = event_id_id_id,
    )
    newScheduleEntity.save()

    return redirect("home")
