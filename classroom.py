import os.path
from datetime import date, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    'https://www.googleapis.com/auth/classroom.student-submissions.students.readonly',
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly'
]

def login(id):
    """
    Loggar in användaren och hämtar ett "credentials". Om vi redan har användarens "credentials" 
    så öpnnar vi dem från filen "database/users/id.json" där idet är användarens discord id. 
    Om filen inte finns skapas en google OAuth för att få dem. 
    """
    creds = None

    if os.path.exists(f'database/users/{id}.json'):
        # Laddar "credentials" från filen om det redan finns.
        creds = Credentials.from_authorized_user_file(f'database/users/{id}.json', SCOPES)
        return 531

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Uppdaterar "credentials" om det skulle vara utdaterade.
            creds.refresh(Request())
        else:
            # Skaper en OAuth. Detta om "credentials" inte skulle finnas innan.
            flow = InstalledAppFlow.from_client_secrets_file(
                'database/google/desktopClientSecretClassroom.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Sparar ner "credentials" till en fil.
        with open(f'database/users/{id}.json', 'w') as token:
            token.write(creds.to_json())
    return


def getCourses(id):
    """
    Hämtar en användarens kurs/kurser. Returnerar en lista med kurser i str.
    """
    creds = None

    # Kontrollerar om användaren redan finns i databasen.
    if os.path.exists(f'database/users/{id}.json'):
        # Hämtar "Credentials" för användaren från database/users/{id}.json.
        creds = Credentials.from_authorized_user_file(f'database/users/{id}.json', SCOPES)

        try:
            # Ropar på Classroom API med "Credentials".
            service = build('classroom', 'v1', credentials=creds)

            # Hämtar en lista med kurser från Classroom API
            results = service.courses().list(pageSize=10).execute()
            courses = results.get('courses', [])

            if not courses:
                # Om inga kurser hittades, returnera 404
                return 404

            strTemplate = ''
            for course in courses:
                # Skapar en sträng som innehåller namnen på kurserna
                strTemplate += f'{course["name"]}\n'

            # Returnerar strängen med kursnamnen
            return strTemplate

        except HttpError as error:
            print('An error occurred: %s' % error)

    # Om "Credentials" har gått ut och det finns en refresh token
    # försök uppdatera "Credentials".
    elif creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    else:
        # Om användaren inte finns i databasen eller om inloggningen misslyckades
        # försöker vi logga in igen och anropa funktionen getCourses(id).
        login(id)
        return getCourses(id)


def extractDueDate(due_date):
    """
    Fomaterar om dueDate och retunerar en lista med år, månad och dag. Tänkt 
    att användas för att sedan lättare jämföra datum från google classroom 
    och datetime modulen.
    """
    # Kontrollerar om due_date är av typen dictionary
    if isinstance(due_date, dict):
        # Extraherar år, månad och dag från due_date-dictionaryn
        year = due_date.get('year')
        month = due_date.get('month')
        day = due_date.get('day')

        # Kontrollerar att år, månad och dag finns och inte är None
        if year is not None and month is not None and day is not None:
            # Returnerar en lista med år, månad och dag
            return [year, month, day]

    # Returnerar en tom lista om due_date inte är en dictionary eller om något
    # av året, månaden eller dagen är None.
    return []


def courseWork(id):
    """
    Hämtar en användares uppgifter i kurser som inte är archiverade. 
    Returnerar uppgifterna i en lista med kursnamn följt av uppgifterna.
    """
    creds = None
    coursework_data = []

    # Kontrollerar om användaren finns i databasen.
    if os.path.exists(f'database/users/{id}.json'):
        # Hämtar "Credentials" för användaren från database/users/{id}.json.
        creds = Credentials.from_authorized_user_file(f'database/users/{id}.json', SCOPES)

        try:
            # Ropar på Classroom API med "Credentials".
            service = build('classroom', 'v1', credentials=creds)

            # Hämtar en lista på kurser från Classroom API.
            results = service.courses().list().execute()
            courses = results.get('courses', [])

            for course in courses:
                course_id = course['id']
                course_name = course['name']
                course_status = course['courseState']

                if course_status != 'ARCHIVED':
                    # Hämtar data för specifik kurs.
                    coursework_results = service.courses().courseWork().list(courseId=course_id).execute()
                    coursework = coursework_results.get('courseWork', [])

                    if coursework:
                        coursework_list = []
                        for work in coursework:
                            courseWorkTitle = work.get('title', 'Untitled')
                            deadline = work.get('dueDate')
                            due_date = extractDueDate(deadline)
                            if due_date:
                                coursework_list.append({'title': courseWorkTitle, 'due_date': due_date})
                            else:
                                coursework_list.append({'title': courseWorkTitle})

                        coursework_data.append({'course_name': course_name, 'coursework': coursework_list})

            # Returnerar en lista med kursnamn följt av uppgifter för den kursen.
            return coursework_data

        except HttpError as error:
            print('An error occurred: %s' % error)

    # Om "Credentials" har gått ut och det finns en refresh token
    # försök uppdatera "Credentials".
    elif creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    else:
        # Om användaren inte finns i databasen eller om inloggningen misslyckades
        # försöker vi logga in igen och anropa funktionen courseWork(id).
        login(id)
        return courseWork(id)


def monthCourseWork(id):
    """
    Hämtar uppgifter inom tids spannet 15 dagar från dagens datum. Använder funktionen 
    extractDueDate() för att jämföra datum. 
    Returnerar uppgifterna i en lista med kursnamn följt av uppgifterna.
    """
    creds = None
    coursework_data = []

    # Kontrollerar om användaren finns i databasen.
    if os.path.exists(f'database/users/{id}.json'):
        # Hämtar "Credentials" för användaren från database/users/{id}.json.
        creds = Credentials.from_authorized_user_file(f'database/users/{id}.json', SCOPES)

        try:
            # Ropar på Classroom API med "Credentials".
            service = build('classroom', 'v1', credentials=creds)

            # Hämtar en lista på kurser från Classroom API.
            results = service.courses().list().execute()
            courses = results.get('courses', [])

            # Beräknar tidsintervallet för 15 dagar från dagens datum.
            today = date.today()
            range_start = today - timedelta(days=15)
            range_end = today + timedelta(days=15)

            # Itererar över kurserna
            for course in courses:
                course_id = course['id']
                course_name = course['name']
                course_status = course['courseState']

                # Kontrollerar om kursen inte är arkiverad.
                if course_status != 'ARCHIVED':
                    # Hämtar uppgifter för specifik kurs.
                    coursework_results = service.courses().courseWork().list(courseId=course_id).execute()
                    coursework = coursework_results.get('courseWork', [])

                    coursework_in_range = False
                    coursework_list = []

                    # Itererar över kursuppgifterna.
                    if coursework:
                        for work in coursework:
                            deadline = work.get('dueDate')
                            due_date = extractDueDate(deadline)
                            if due_date:
                                work_date = date(due_date[0], due_date[1], due_date[2])
                                # Kontrollerar om uppgiften ligger inom tidsintervallet.
                                if range_start <= work_date <= range_end:
                                    coursework_in_range = True
                                    coursework_list.append(work)

                    # Lägger till kursen och uppgifterna i resultatlistan om det finns uppgifter inom tidsintervallet.
                    if coursework_in_range:
                        coursework_data.append({'name': course_name, 'coursework': coursework_list})

            # Returnerar uppgifter inom tidspannet 15 dagar.
            return coursework_data

        except HttpError as error:
            return f'An error occurred: {error}'

    # Om "Credentials" har gått ut och det finns en refresh token
    # försök uppdatera "Credentials".
    elif creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    else:
        # Om användaren inte finns i databasen eller om inloggningen misslyckades
        # försöker vi logga in igen och anropa funktionen courseWork(id).
        login(id)
        return monthCourseWork(id)

    
def weekCourseWork(id):
    """
    Hämtar uppgifterna för den kommande veckan. Använder datetime-modulen 
    och funktionen extractDueDate() för att jämföra datum. 
    Returnerar uppgifterna i en lista med kursnamn följt av uppgifterna.
    """
    creds = None
    coursework_data = []

    # Kontrollerar om användaren finns i databasen.
    if os.path.exists(f'database/users/{id}.json'):
        # Hämtar "Credentials" för användaren från database/users/{id}.json.
        creds = Credentials.from_authorized_user_file(f'database/users/{id}.json', SCOPES)

        try:
            # Ropar på Classroom API med "Credentials".
            service = build('classroom', 'v1', credentials=creds)

            # Hämtar en lista på kurser från Classroom API.
            results = service.courses().list().execute()
            courses = results.get('courses', [])

            # Beräknar start- och slutdatum för veckan.
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)

            # Itererar över kurserna
            for course in courses:
                course_id = course['id']
                course_name = course['name']
                course_status = course['courseState']

                # Kontrollerar om kursen inte är arkiverad.
                if course_status != 'ARCHIVED':
                    # Hämtar data för specifik kurs.
                    coursework_results = service.courses().courseWork().list(courseId=course_id).execute()
                    coursework = coursework_results.get('courseWork', [])

                    coursework_in_range = False
                    coursework_list = []

                    # Itererar över kursuppgifterna.
                    if coursework:
                        for work in coursework:
                            deadline = work.get('dueDate')
                            due_date = extractDueDate(deadline)
                            if due_date:
                                work_date = date(due_date[0], due_date[1], due_date[2])
                                # Kontrollerar om uppgiften ligger inom datumen för veckan.
                                if week_start <= work_date <= week_end:
                                    coursework_in_range = True
                                    coursework_list.append(work)

                    # Lägger till kursen och uppgifterna i listan om det finns uppgifter inom veckan.
                    if coursework_in_range:
                        coursework_data.append({'name': course_name, 'coursework': coursework_list})

            # Returnerar uppgifter för den kommande veckan som en lista
            return coursework_data

        except HttpError as error:
            return f'An error occurred: {error}'

    # Om "Credentials" har gått ut och det finns en refresh token
    # försök uppdatera "Credentials".
    elif creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    else:
        # Om användaren inte finns i databasen eller om inloggningen misslyckades
        # försöker vi logga in igen och anropa funktionen courseWork(id).
        login(id)
        return weekCourseWork(id)


if __name__ == '__main__': # undviker situation när koden kopplas som en modul och kör sig själv
    # login()
    # getCourses()
    # courseWork()
    # weekCourseWork()
    pass
