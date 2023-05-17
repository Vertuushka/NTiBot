# Filen tillhör NTiBot projekt.
# Filen innehåller funktioner som jobbar med schoolsoft API
import schoolsoft_api
import json
from datetime import datetime
import DBHandler

school = "nti"
def login(id,school=school):
    """
    Funktionen loggar in användaren till SchoolSoft genom att läsa användarinformation
    från en fil och hämta en applikationsnyckel. Funktionen tar två argument: id,
    som representerar användarens identitet, och school, som representerar skolan.
    För vår bot, skolan har konstant namn "NTI"
    """
    
    # Öppnar och läser användarinformationen
    with open(f'database/SDB/{id}.txt','r') as userData:
        user = userData.readlines()
        DBHandler.cleanData(user)
    # Hämta användernamn och lösenord
    name = user[1] # Användernamn
    password = user[2] #Lösenord

    # Får en applikationsnyckel genom att logga in på SchoolSoft
    app_key = schoolsoft_api.get_app_key(name, password, school)

    # Hämtar organisations-ID:et från applikationsnyckeln
    org_id = app_key['orgs'][0]['orgId']
    # Uppdaterar token för användaren
    token = schoolsoft_api.get_updated_token(school, app_key_json=app_key, token_path=f"datbase/scache/{id}.json")['token']
    # Hämtar lektionerna för användaren
    schoolsoft_api.get_lessons(token,school,org_id)

def is_lesson_today(lesson, current_week, current_day):
    """
    Funktionen kontrollerar om en specifik lektion är planerad för idag baserat på
    lektionens vecka och dag. Funktionen tar tre argument: lesson, som representerar
    lektionen, current_week, som representerar den aktuella veckan, och current_day,
    som representerar den aktuella dagen.
    """

    # Delar upp veckorna när lektionen är planerad
    weeks = lesson["weeksString"].split(", ")
    # Loopar igenom veckointervallerna
    for week_range in weeks:
        # Om det är ett intervall av veckor
        if "-" in week_range:
            # Ta fram start- och slutveckan för intervallet
            start_week, end_week = map(int, week_range.split("-"))
            # Om den nuvarande veckan ligger inom intervall och om lektionen är idag
            if start_week <= current_week <= end_week and lesson["dayId"] == current_day:
                return True
        # Om det är en enskild vecka
        else:
            try:
                # Konvertera veckonumret till en integer
                week_number = int(week_range)
                # Om den nuvarande veckan är veckan när lektionen är planerad och om lektionen är idag
                if week_number == current_week and lesson["dayId"] == current_day:
                    return True
            # Om veckonumret inte kan konverteras till en integer, returnera False
            except ValueError:
                return False
    # Om ingen matchning hittas, returnera False
    return False

def is_lesson_this_week(lesson, current_week):
    """
    Funktionen kontrollerar om en specifik lektion är planerad för den här veckan.
    Funktionen tar två argument: lesson, som representerar lektionen, och current_week,
    som representerar den aktuella veckan.
    """

    # Delar upp veckorna när lektionen är planerad
    weeks = lesson["weeksString"].split(", ")
    # Loopar igenom veckointervallerna
    for week_range in weeks:
        # Om det är ett intervall av veckor
        if "-" in week_range:
            # Ta fram start- och slutveckan för intervallet
            start_week, end_week = map(int, week_range.split("-"))
            # Om den nuvarande veckan ligger inom intervall
            if start_week <= current_week <= end_week:
                return True
        # Om det är en enskild vecka
        else:
            try:
                # Konvertera veckonumret till en integer
                week_number = int(week_range)
                # Om den nuvarande veckan är veckan när lektionen är planerad
                if week_number == current_week:
                    return True
            # Om veckonumret inte kan konverteras till en integer, returnera False
            except ValueError:
                return False
    # Om ingen matchning hittas, returnera False
    return False

def todayLessons(id):
    """
    Funktionen hämtar och returnerar dagens lektioner för en specifik användare.
    Funktionen tar ett argument: id, som representerar användarens identitet.
    """

    # Loggar in användaren och hämtar lektioner 
    login(id)
    # Öppnar och laddar lektioner från json-filen
    with open("lessons.json", "r") as file:
        lessons = json.load(file)
    # Hämtar dagens datum och tid
    today = datetime.now()
    # Räknar ut aktuell vecka och dag
    current_week = today.isocalendar()[1]
    current_day = today.weekday()
    # Initierar variabler för att lagra dagens lektioner, rum och starttider
    todayLessons = ''
    todayLessons = ''
    todayRooms = []
    todayStart = []

    # for i in range(len(lessons)):
    #     todayLessons.append(is_lesson_today(lessons[i],current_week,current_day))

    # Skapar en lista av dagens lektioner som matchar veckan och dagen
    lessons_today = [lesson for lesson in lessons if is_lesson_today(lesson, current_week, current_day)]
    # Sorterar lektionerna efter starttid
    lessons_today.sort(key=lambda lesson: lesson["startTime"])
    print(f"Current week: {current_week}, current day: {current_day}")
    # Loopar genom dagens lektioner
    for lesson in lessons_today:

        # Formaterar och lägger till lektionens information till todayLessons
        # subject = lesson["subjectName"].split('-')[0]
        todayLessons += f'**{datetime.strptime(lesson["startTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M")} - {datetime.strptime(lesson["endTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M")}**\n{lesson["subjectName"].split("-")[0]} i {lesson["roomName"]}\n\n'

        # Lägger till lektionens rum till todayRooms
        # room = lesson["roomName"]
        todayRooms.append(lesson["roomName"])

        # Formaterar och lägger till lektionens starttid till todayStart
        # start_time = datetime.strptime(lesson["startTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M")
        todayStart.append(datetime.strptime(lesson["startTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M"))

        # print(f"{subject} - Room: {room} - Start time: {start_time}")

    # Returnerar dagens lektioner, rum och starttider
    return(todayLessons,todayRooms,todayStart)
# print(todayLessons())


def weekLessons(id):
    """¨
    Funktionen bearbetar information från schoolsoft för att
    visa användare veckans schemat. Funktionen refererar till
    en annan funktion login som skapar lessons.json fil där
    ligger allt information om användares lektioner. 
    Därefter bearbetas information och returneras i form av 
    lektionslista. Endast problem med funktionen är att om 
    det är flera användare som vill se schemat samtidigt
    kan det uppstå fel med lektionerna, eftersom lessons.jsom
    överskrivs för alla.
    För att skilja dagar används speciella markörer som läggs till
    varje sträng beroende på vilken dayId har lektionen som bearbetas:
    $0$ - Måndag
    $1$ - Tisdag
    $2$ - Onsdag
    $3$ - Torsdag
    $4$ - Fredag

    arg:
        id - user id av personen som anropar funktionen
    """
    login(id) # loggar in användare och skapar lessons.json 
    with open("lessons.json", "r") as file: # läser lessons.json
        lessons = json.load(file)
    today = datetime.now() # vilken dag är idag
    current_week = today.isocalendar()[1] # vad är det för vecka
    weekLessonsList = [] # en tom lista för att senare appenda lektioner
    lessons_today = [lesson for lesson in lessons if is_lesson_this_week(lesson, current_week)]
    for lesson in lessons_today: # itererar lektioner
        # koden nere skapar strängar med rätt formatering och markerar sträng
        if lesson["dayId"] == 0:
            weekLessonsList.append(f'> **{datetime.strptime(lesson["startTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M")}\t - \t{datetime.strptime(lesson["endTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M")}**$0$\t ・ \t{lesson["subjectName"].split("-")[0]} ({lesson["roomName"]})$0$\n')
        if lesson["dayId"] == 1:
             weekLessonsList.append(f'> **{datetime.strptime(lesson["startTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M")} - {datetime.strptime(lesson["endTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M")}**$1$ - {lesson["subjectName"].split("-")[0]} ({lesson["roomName"]})$1$\n')
        if lesson["dayId"] == 2:
             weekLessonsList.append(f'> **{datetime.strptime(lesson["startTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M")} - {datetime.strptime(lesson["endTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M")}**$2$ - {lesson["subjectName"].split("-")[0]} ({lesson["roomName"]})$2$\n')
        if lesson["dayId"] == 3:
             weekLessonsList.append(f'> **{datetime.strptime(lesson["startTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M")} - {datetime.strptime(lesson["endTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M")}**$3$ - {lesson["subjectName"].split("-")[0]} ({lesson["roomName"]})$3$\n')
        if lesson["dayId"] == 4:
            weekLessonsList.append(f'> **{datetime.strptime(lesson["startTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M")} - {datetime.strptime(lesson["endTime"], "%Y-%m-%d %H:%M:%S.0").strftime("%H:%M")}**$4$ - {lesson["subjectName"].split("-")[0]} ({lesson["roomName"]})$4$\n')
    return(weekLessonsList,current_week)

if __name__ == '__main__': # undviker situation när koden kopplas som en modul och kör sig själv
    pass