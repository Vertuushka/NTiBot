# Filen tillhör NTiBot projekt.
# Filen innehåller alla funktioner som kan användas för att jobba med botens databas.
# Botens databas har följande struktur:
#   - /database         - databasens huvudmapp
#   - /database/google/ - lägg din kopplade användare från google cloud här
#   - /database/SDB/    - schoolsoft databas, där sparas användarnas info som .txt fil
#   - /database/users/  - google databas, där sparas alla user tokens som .json filer
# alla funktioner tar id som ett argument, vilket behövs för att kunna skilja användare och
# skapa unika filnamn
import os
import os.path
import config

# funktionen som tar bot obehöriga symboler från .txt filer
def cleanData(array):
    for i in range(len(array)):
        array[i] = array[i].replace(' ','')
        array[i] = array[i].replace('\n', '')

#__________SCHOOLSOFT DB__________
    

def getSecure(id):
    """
    Funktionen kontrollerar om användare finns i databas. Om ja - returnerar användarnamn och krypterat lösenord.
    Används för att kunna se inlogningsstatus.
    arg:
        id - användares discordID (används för unika filnamn)
    """
    if os.path.isfile(f'database/SDB/{id}.txt'):
        with open(f'database/SDB/{id}.txt','r') as cUser:
            cData = cUser.readlines()
            cleanData(cData)
            login = cData[1]
            if len(cData) > 2: # om användare redan skrivit lösenord
                password = cData[2]
                key = ''
                for i in range(len(password)): # ändrar alla symboler i lösenord till # (* avnänds redan i discords formatering)
                    key += '#'
                return(login, key)
            else:
                return(login,'Not applied') # om inte lösenord finns - 'not applied'
    else:
        return(404) # config.userNotFound

# funktioner som skapar en ny fil i databas och skriver in användares discord ID samt schoolsoft användarnamn.
def appendUser(id, login):
    """
    Funktionen skapar en ny fil i databas och skriver in användarens discordID samt schoolsofts användarnamn.
    arg:
        id      - användares discordID (används för unika filnamn och användare identifiering inuti DBfil)
        login   - användares användarnamn (skrivs tillsammans med inloggnings kommando)
    """
    if not os.path.isfile(f'database/SDB/{id}.txt'):
        with open(f'database/SDB/{id}.txt', '+w') as cUser:
            cUser.write(f'{id}\n{login}\n')
            return(config.loginSaved)
    else:
        return(config.passwordExists)      

def appendPassword(id,password):
    """
    Funktionen lägger till lösenord till en redan existerade användares fil i databas.
    arg:
        id          - användares discordID (används för unika filnamn och användare identifiering)
        password    - användares lösenord (skrivs tillsammans med inloggnings kommando)
    """
    if os.path.isfile(f'database/SDB/{id}.txt'):
        with open(f'database/SDB/{id}.txt', '+a') as cUser:
            cUser.write(f'{password}\n')
            return(config.passSaved)
    else:
        return(config.userNotFound)

def sRemove(id):
    """
    Funktionen utloggar (tar bort filen från databasen) anävndare från schoolsoft.
    arg:
        id - användares discordID (används för unika filnamn och användare identifiering)
    """
    try:
        path = f'database/SDB/{id}.txt'
        os.remove(path)
        return(config.softOut)
    except:
        return(404) # om användare inte är med i databas


#__________CLASSROOM DB__________

def resetgInfo(id):
    """
    Funktionen utloggar (tar bort användares token) anävndare från classroom.
    arg:
        id - användares discordID (används för unika filnamn och användare identifiering)
    """
    if os.path.isfile(f'database/users/{id}.json'):
        path = f'database/users/{id}.json'
        os.remove(path)
    else:
        return(404) # om användare inte är med i databas
    

if __name__ == '__main__': # undviker situation när koden kopplas som en modul och kör sig själv
    pass