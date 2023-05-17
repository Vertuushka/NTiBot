# Filen tillhör NTiBot projekt.
# Filen innehåller alla texter som kan synas i gränsnitten.

# Botens token placeras här
token = ' ' 

# text START

helpBot = """Välkommen till **NTiBot**! :fox: 
Här kommer en lista av det jag kan göra:

**Classroom**
**`!glogin`** Logga in.

**`!gout`** Logga ut.

**`!gclass`** Lista på kurser.

**`!gwork`** Lista på alla uppgifter.

**`!gweek`** Inlämningar denna vecka.

**`!gmonth`** Inlämningar denna månad.


**Schoolsoft**
**`!ssoft`** Inloggnings info: inloggad/inte inloggad, därefter följ skickade instruktioner.

**`!slogin`** + **`ditt användarnamn`** SKRIV EJ "+", därefter följ skickade instruktioner.

**`!spass`** + **`ditt lösenord`** SKRIV EJ "+", använd **`!slogin`** först.

**`!schedule`** Visa dagens schema.

**`!wschedule`** Visa veckans schema.

**Övrigt**
**`!hibot`** Säg "hej" till bot.

**`!test`** Bara utvecklare har åtkomst till kommandon.
"""
# helptext END

# några bilder som bifogas 
botImg = 'https://media.discordapp.net/attachments/957552535122616333/1103664900053680160/img.png?'
schoolSoftImg = 'https://play-lh.googleusercontent.com/mTNMh0pombnh06rbkAjySII-gpTkPt7c0wyfgQiJxG2lOVqBdPPr9uTICxwVqhiGMlk'
hiGif = 'https://tenor.com/view/fox-blinking-checks-phone-gif-17886696'
developer = 'https://media.discordapp.net/attachments/920286440838033468/1105028189627088916/Namnlost-1.png?width=500&height=500'
logoutImg = 'https://tenor.com/blmsV.gif'
gClassImg = 'https://upload.wikimedia.org/wikipedia/commons/5/59/Google_Classroom_Logo.png'
gClassEmbedIcon = 'https://media.discordapp.net/attachments/957552535122616333/1103716492119392338/icons8-finger-pointing-down-94.png?width=117&height=117'

#__________CLASSROOM__________
gClassMain = 'https://classroom.google.com/'
gClassLogin = 'Du är inloggad!'
gClassMainBtn = 'Gå till Classroom'
gClassEmbedFooter = 'Tryck på knappen för att öppna i webbläsare'
gLogInProcessing = 'Jag bekräftar din inloggning. Processen kan ta lite tid. Jag meddelar dig när du ät inloggad.'
logout = 'Du har blivit utloggad.'
noWork = 'Du har inga uppgifter. Du är fri! :tada:'
gmonthWarning = '`Uppmärksamma! Uppgifternas inlämningsdatum ligger i tidspanet 15 dagar från dagens datum.`'
workLoading = 'Frågar dina lärare. :man_raising_hand: '
yourLessons = 'Dina uppgifter'
yourLessonsMonth = 'Dina uppgifter för månaden'
yourCourses = 'Dina kurser'
gloginError = 'Google verkar vara på lunch. Lyckades inte att hämta dina uppgifter. :c\nFörsök igen eller kontakta utvecklare.'
loginGoogle = 'Använd `!glogin` först.'

#__________SCHOOLSOFT__________
userNotFound = 'Dina uppgifter finns inte i databas/cache. Försök att logga in först.' #fel 404
alreadyTaken = 'Det finns redan ett konto med angivna användarnamn och lösenord. Försör att återställa dina uppgifter.' #fel 405
tokenExists = 'Du är redan inloggad. För att logga ut använd `!glogout`' #fel 531
missingPassword = 'Det verkara vara fel med ditt lösenord. Försök igen, logga ut eller kontakta uvecklare.' #fel 401
missingLogin = 'Det verkar vara fel med ditt användarnamn. Försök igen, logga ut eller kontakta uvecklare.' #fel 401
passwordExists = 'Du är redan inloggad. Logga ut för att ändra information.' #fel 58
privateChat = 'Av säkerhetsskäl förtsätt chatten privat! :eyes:'
useLogin = 'Använd `!slogin *Ditt schoolsofts användarnamn*`'
usePass = 'Nästa steg är att spara lösenord. Använd `!spass *ditt schoolsofts lösenord*`.'
yourData = 'Du är inloggad med följande uppgifter:'
username = 'Användarnamn'
password = 'Lösenord'
savePass = 'Sparar ditt lösenord...'
saveUsername = 'Sparar ditt användarnamn...'
loginSaved = 'Ditt användarnamn är sparat!'
passSaved = 'Ditt lösenord är sparat!'
softOut = 'Du har blivit utloggad!'
deleteData = 'Kastar ut din information genom fönstret. :window:'
yourScheduleToday = 'Dina lektioner idag'
yourScheduleWeek = 'Dina lektioner (v. '
monday = 'Måndag'
tuseday = 'Tisdag'
wednesday = 'Onsdag'
thursday = 'Torsdag'
friday = 'Fredag'
softLogin = 'Dina uppgifter inte stämmer. Kontrollera inloggningsstatus genom `!ssoft` eller logga ut och försök igen.'

#__________ANNAT__________

hiBot = 'Hej! Jag är NtiBot v.1.1 (release).\nDu kan kontakta mina utvecklare via discord:\n> eerikazz#6028 (google API)\n> LordTenebris#9325 (schoolsoft API)\n> Vertushka#8337 (UX, discord API)'
embedError = 'Jag mysslyckades med att visa dig information. Försök igen eller kontakta utvecklare.'
thelp = 'Hjälp'