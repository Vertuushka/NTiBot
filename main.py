# Filen tillhör NTiBot projekt.
# Filen innehåller huvukoden som kopplar alla andra delat tillsammans.
import discord
from discord.ext import commands
import classroom
import schoolsoft
import DBHandler
import config

# botens konfiguration. Bestämmer åtkomst och skapar shälva boten
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
# skapar bot och ändrar åtkomst, prefix för kommando och inaktiverar standart hjälp
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None) 

# skickar en del information när boten är inloggad samt synkroniserar botens kommandon med discord slash commands
@bot.event
async def on_ready(): 
    print("ready")
    await bot.tree.sync()

def embedTemplate(title,description,img='bot',color=discord.Color.dark_orange(),footer=None):
    """
    Funktionen skapar en embed-message och behöver ett antal argument:
    title vilket är messages rubrik (string)
    description där skriv själva texten (string)
    img för att lägga till en bild (standartvärde - botens bild, string)
    color för att hantera färg på den vänstra sida (standartvärde - orange, funktion)

    Några typiska color-värde som boten använder:
    discord.Color.dark_green()
    discord.Color.dark_blue()
    nothing to orange

    Argementet img kan endast ta följade:
    gclass = classroom logo 
    bot = bot logo
    anything else to schoolsoft

    Footer anävnds för att skapa footer om den behövs:
    None = standart värde som skapar ingen footer
    gclass = tryck på knappen template (str)
    """
    try:
        embed = discord.Embed(
        title=title, # rubrik
        description=description, # själva meddelandets text
        color=color ) # färg
        # nedstående rader lägger till bild.
        if img == 'bot':
            embed.set_thumbnail(url=config.botImg)
        elif img == 'gclass':
            embed.set_thumbnail(url=config.gClassImg)            
        elif img == 'dev':
            embed.set_thumbnail(url=config.developer)
        elif img == 'none':
            pass
        else:
            embed.set_thumbnail(url=config.schoolSoftImg)
        # lägger till footer om den vehövs
        if footer != None:
            if footer == 'gclass':
                embed.set_footer(text=config.gClassEmbedFooter,icon_url=config.gClassEmbedIcon)
        # embed.set_footer(text='Here is the footer',icon_url='https://upload.wikimedia.org/wikipedia/commons/5/59/Google_Classroom_Logo.png')
        return embed
    except:
        # om något gick fel
        return(config.embedError)

def getAuthor(ctx):
    """
    Funktionen ger möjlighet att ta ID av användare som skickat ett
    meddelande. Funktionen behöver ett argument ctx som också
    skickas till alla kommando och representerar meddelandets context.
    """
    client = str(ctx.message.author.id)
    return(client)

class LinkBtn(discord.ui.View):
    def __init__(self, name, url):
        """classen skapar knappar med länkar och behöver därför två argement:
        name = namn, text som ska visas på knappen (str)
        url = länken som man ska gå till när man trycker på knappen (str)
        """
        super().__init__()
        self.add_item(discord.ui.Button(label=name, url=url))

def courseHandler(data):
    """
    Funktionen bearbetar information som tas ur classroom.
    Argument 'data' är den information man får från classroom.
    """
    if not data:
        return(config.noWork)
    else:
        coursework_string = "" # variabel där sparas formaterat data
        for course_data in data:
            course_name = course_data['name'] # tar kursens namn
            coursework_list = course_data['coursework'] # tar uppgiftens namn
            coursework_string += f"**{course_name}**\n"
            for work in coursework_list:
                courseWorkTitle = work.get('title', 'Untitled') # tar uppgiftens rubrik
                deadline = work.get('dueDate') # tar inlämningsdatum
                due_date = classroom.extractDueDate(deadline)
                if due_date:
                    coursework_string += f"> **{due_date[0]}/{due_date[1]}/{due_date[2]}**\n> {courseWorkTitle}\n" # formaterar info
                else:
                    coursework_string += f"> {courseWorkTitle}\n" # om det inte finns inlämningsdatum
            coursework_string += "\n"
    return(coursework_string)

@bot.hybrid_command() #skickar hjälp
async def help(ctx):   
    """Manual som förklarar alla kommandon."""
    await ctx.send(embed=embedTemplate(config.thelp,config.helpBot))

@bot.hybrid_command() # säg "hej" till boten och få lite information
async def hibot(ctx):
    """Säg "hej" till boten och få lite information"""
    await ctx.send(config.hiGif)
    await ctx.send(config.hiBot)

@bot.hybrid_command()
async def manual(ctx):
    """Skickar en pdf manual"""
    await ctx.reply(file=discord.File("database/NTiBot-Manual.pdf"))
    
#__________GOOGLE SECTION__________

@bot.hybrid_command() #logga in i google-konto
async def glogin(ctx):
    """Logga in i google-konto"""
    await ctx.reply(config.gLogInProcessing) # meddelande om att processen är igång
    # Föregående rad behövs för att slippa fel som uppsåtr pga hybrid commands logiken. 
    # Om den inte får svar från programmet under 3 sekunder så skickar den fel per automatik vilket vi vill unvdvika.
    # Därför meddelar vi användare först att programmet ska köras nu, kör själva logiken och meddelar i programmets slut.
    try:
        if classroom.login(getAuthor(ctx)) == 531: 
            await ctx.send(config.tokenExists) # om anävndare är redan inloggad 
        else: 
            await ctx.send(config.gClassLogin)
    except:
        await ctx.send(config.gloginError) # om något gick fel (väldigt osannolikt)...
        
@bot.hybrid_command() #logga ut från google-konto
async def gout(ctx):
    """Logga ut från google-konto"""
    if DBHandler.resetgInfo(getAuthor(ctx)) != 404: # kontrollerar om användare som vill logga ut är inloggat
        await ctx.reply(config.logout)
    else:
        await ctx.reply(config.userNotFound)

@bot.hybrid_command() #visar alla kurser från google classroom
async def gclass(ctx):
    """Se alla dina kurser i classroom"""
    await ctx.reply(config.workLoading)
    courses = classroom.getCourses(getAuthor(ctx))
    await ctx.send(
        embed=embedTemplate(f"{config.yourCourses}\n{str(ctx.message.author)}", courses,'gclass',discord.Color.dark_green(),'gclass'),
        view=LinkBtn(config.gClassMainBtn,config.gClassMain))

@bot.hybrid_command()
async def gweek(ctx):
    """Se alla inlämningar denna veckan"""
    await ctx.reply(config.workLoading)
    coursework_string = courseHandler(classroom.weekCourseWork(getAuthor(ctx)))
    await ctx.send(embed=
    embedTemplate(f"{config.yourLessons}\n{str(ctx.message.author)}", f'\n\n{coursework_string}', 'gclass', discord.Color.dark_green()))

@bot.hybrid_command()
async def gmonth(ctx):
    """Se alla inlämningar denna månad"""
    # coursework_data =  
    await ctx.reply(config.workLoading)
    data = courseHandler(classroom.monthCourseWork(getAuthor(ctx))) 
    await ctx.send(embed=
    embedTemplate(f"{config.yourLessonsMonth}\n{str(ctx.message.author)}", f'{config.gmonthWarning}\n\n{data}', 'gclass', discord.Color.dark_green()))


#__________ SCHOOLSOFT SECTION__________

@bot.hybrid_command()
async def ssoft(ctx):
    """Se din status i schoolsoft (inloggat/utloggad)"""
    await ctx.reply(config.privateChat)
    info = DBHandler.getSecure(getAuthor(ctx))
    if info == 404:
        await ctx.message.author.send(config.useLogin)
    else:
        await ctx.message.author.send(f'{config.yourData}\n{config.username} {info[0]}\n{config.password} {info[1]}')

@bot.hybrid_command()
async def slogin(ctx,text='Empty'):
    """Lägga till ditt schoolsoft användarnamn"""
    await ctx.reply(config.saveUsername)
    info = DBHandler.getSecure(getAuthor(ctx))
    if text != 'Empty' and info != 404: 
        await ctx.message.author.send(f'{config.yourData}\n{config.username} {info[0]}\n{config.password} {info[1]}')
    elif text != 'Empty' and "." in text:
        await ctx.message.author.send(DBHandler.appendUser(getAuthor(ctx),text))
        await ctx.message.author.send(config.usePass)
    else:
        await ctx.message.author.send(config.missingLogin)

@bot.hybrid_command()
async def spass (ctx,text='Empty'):
    """Lägga till ditt schoolsoft lösenord"""
    await ctx.reply(config.savePass)
    info = DBHandler.getSecure(getAuthor(ctx))
    if info != 404:
        if info[1] != 'Not applied':
            await ctx.message.author.send(config.passwordExists)
        elif text != 'Empty':
            await ctx.message.author.send(DBHandler.appendPassword(getAuthor(ctx),text))
        else:
            await ctx.message.author.send(config.missingPassword)
            # schoolsoft.createToken(id)
    else: 
        await ctx.message.author.send(config.useLogin)

@bot.hybrid_command()
async def sout(ctx):
    """Logga ut från schoolsoft"""
    await ctx.reply(config.deleteData)
    info = DBHandler.getSecure(getAuthor(ctx))
    if info != 404: 
        await ctx.send(DBHandler.sRemove(getAuthor(ctx)))
    else:
        await ctx.send(config.userNotFound)  

@bot.hybrid_command()
async def schedule(ctx):
    """Se dagens schema"""
    try:
        lesArray = schoolsoft.todayLessons(getAuthor(ctx))
        await ctx.send(embed=embedTemplate(f'{config.yourScheduleToday}\n__{str(ctx.message.author)}__',f'\n{lesArray[0]}','123',discord.Color.dark_blue()))
    except:
        await ctx.send(config.softLogin)
    # schoolsoft.getSchedule()

@bot.hybrid_command()
async def wschedule(ctx):
    """Se veckans schema"""
    try:
        lesArray = schoolsoft.weekLessons(getAuthor(ctx)) # får information från schoolsoft
        embed=embedTemplate(f'{config.yourScheduleWeek}{lesArray[1]})\n__{str(ctx.message.author)}__',f'','123',discord.Color.dark_blue())
        wlessons = lesArray[0]
        # sorterar data
        monLess = ''
        tueLess = ''
        wedLess = ''
        thuLess = ''
        friLess = ''
        # tar bort dag-markörer från texten och sorterar.
        for i in range(len(wlessons)):
            if '$0$' in wlessons[i]:
                wlessons[i] = wlessons[i].replace('$0$','')
                monLess+=wlessons[i]
            if '$1$' in wlessons[i]:
                wlessons[i] = wlessons[i].replace('$1$','')
                tueLess+=wlessons[i]
            if '$2$' in wlessons[i]:
                wlessons[i] = wlessons[i].replace('$2$','')
                wedLess+=wlessons[i]
            if '$3$' in wlessons[i]:
                wlessons[i] = wlessons[i].replace('$3$','')
                thuLess+=wlessons[i]
            if '$4$' in wlessons[i]:
                wlessons[i] = wlessons[i].replace('$4$','')
                friLess+=wlessons[i]
        # skapar en separat sektion för värje dag
        embed.add_field(
            name = f'\n{config.monday}', # rubrik (dag)
            value = monLess, # beskrivning (lektioner)
            inline=False # gör att alla sektioner ligger under varandra
            )
        embed.add_field(
            name = f'\n{config.tuseday}',
            value = tueLess,
            inline=False)
        embed.add_field(
            name = f'\n{config.wednesday}',
            value = wedLess,
            inline=False)
        embed.add_field(
            name = f'\n{config.thursday}',
            value = thuLess,
            inline=False)
        embed.add_field(
            name = f'\n{config.friday}',
            value = friLess,
            inline=False)
        await ctx.send(embed=embed) # sckickar skapade konstruktion
    except:
        await ctx.send(config.softLogin)
    
@bot.command()
async def test(ctx): # funktioner som används för tester.
    """Developer tool."""
    author = getAuthor(ctx)
    if author != ' ': # skriv in utvecklarens ID
        await ctx.reply(embed=embedTemplate('Developer only','You have no access to this command.', img='dev'))
    else:
        await ctx.reply('Hi, Developer!')

bot.run(config.token)