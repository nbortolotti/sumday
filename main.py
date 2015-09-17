__author__ = 'nicolasbortolotti'

import dateutil.parser
import exceptions
import datetime
import sys

from apiclient import sample_tools


def main(argv):
    calendar = raw_input('calendar: ')
    startDateAnalysis = raw_input('Start Date Analysis YYYY-MM-DD: ')
    endDateAnalysis = raw_input('End Date Analysis YYYY-MM-DD:  ')

    syear, smonth, sday = map(int, startDateAnalysis.split('-'))
    cstartDateAnalysis = datetime.date(syear, smonth, sday)

    eyear, emonth, eday = map(int, endDateAnalysis.split('-'))
    cendDateAnalysis = datetime.date(eyear, emonth, eday)


    service, flags = sample_tools.init(argv, 'calendar', 'v3', __doc__, __file__,
                                       scope='https://www.googleapis.com/auth/calendar')

    keysum = ['#sumday', '#sum']
    now = datetime.datetime.now()
    now_plus_thirtydays = now + datetime.timedelta(days=7)
    page_token = None
    sumtime = int(0)
    demo = int(0)
    while True:

        events = service.events().list(
            calendarId=calendar,
            singleEvents=True,
            orderBy='startTime',
            timeMin=cstartDateAnalysis.strftime('%Y-%m-%dT%H:%M:%S-00:00'), #now.strftime('%Y-%m-%dT%H:%M:%S-00:00'),
            timeMax=cendDateAnalysis.strftime('%Y-%m-%dT%H:%M:%S-00:00'), #now_plus_thirtydays.strftime('%Y-%m-%dT%H:%M:%S-00:00'),
            pageToken=page_token,
        ).execute()

        #open file
        myfile = open(calendar + '.txt', 'wb')

        for event in events['items']:
            try:
                content = event['description'].encode('utf-8')
                if any(x in content.split() for x in keysum):
                    #print event['summary']
                    myfile.write('*' + event['summary'] + "\n")

                    end = dateutil.parser.parse(event['end']['dateTime'])
                    start = dateutil.parser.parse(event['start']['dateTime'])
                    cal = end - start
                    mins = int(cal.total_seconds() / 60)
                    sumtime += mins

            except exceptions.KeyError:
                pass


        demo = TimeCal(events['items'], keysum)

        page_token = events.get('nextPageToken')
        if not page_token:
            break

    #print("{} - {}".format("minutes", sumtime))


    myfile.write( '** minutes used this week: ' + str(sumtime) + "\n")
    myfile.write( '** demo: ' + str(demo) + "\n")
    myfile.close()


def TimeCal(items={}, keysum=[]):
        #keysum = ['#sumday', '#sum']
        sumtime = int(0)
        for event in items:
            try:
                content = event['description'].encode('utf-8')
                if any(x in content.split() for x in keysum):

                    end = dateutil.parser.parse(event['end']['dateTime'])
                    start = dateutil.parser.parse(event['start']['dateTime'])
                    cal = end - start
                    mins = int(cal.total_seconds() / 60)
                    sumtime += mins

            except exceptions.KeyError:
                pass
        return sumtime

if __name__ == '__main__':
    main(sys.argv)
