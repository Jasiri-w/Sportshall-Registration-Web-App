import schedule
import time
#from .updates import *

def startJobs():

    # Refresh event instance table every 10 minutes
    schedule.every(10).minutes.do(updateInstanceModel).tag("InstanceCron", "Django")

    while True:
        schedule.run_pending()
        time.sleep(1)

def clearJobs():

    #clear all scheduled cron jobs
    schedule.clear()

def getJobs():

    # Return all cron jobs
    schedule.get_jobs()

def cancelJob(job):

    # Cancel a specific job
    schedule.cancel_job(job)
