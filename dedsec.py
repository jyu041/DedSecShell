import threading, time, os, requests, urllib3, click, random
from fake_useragent import UserAgent

# This is the skull to make the main menu look cool
skull = '''             
       *1▒g▒#▒$▒▒1▒,Q        
      ▒▒▒▒▒▒▒▒▓▒▒▒▒▒         
     #/▒▒▒▒▓▒▒▒▓▒▒▓▒g        
     1▒▒▒▒▒‎▒▒▒▓▓▓▒▒▒▒▓\      
     /@ $@@,0▒▒1▒|7$e$,      
           4j7▒4!                ____  ___________  ______ ____________
    |       #7Y*       \        / __ \/ ____// __ \/ ____// ___// ____/\\
    4▒    #▒4▒▓9      4        / / / / __/ // / / /\__ \ / __/ / /\___\/
    $▒9g e@▒▒!4▒▒$-  #e       / /_/ / /___// /_/ /___/ // /___/ /_/__
    |▒▒▒▒▒#|   |e▓▒▒▓$e      /_____/_____//_____//____//_____/\_____/\\
     Yeg▒▓\,   $9▒▒▒e÷4      \_____\\\\____\\\\____ \\\\____\\\\_____\_\____\/
     gp@l▒▒,▒▒Y@▒▒M7 7       
     , ▒▒@1▒▒▒▓9÷▒▒4Q           ______ __  __ _______ ___     ___
        "▓  /Q▒-▒▒7,0$         / ____// /_/ // _____//  /\\   /  /\\
     !     ▒▒                  \__ \ / ___ // ___/  /  / /  /  / /
     \▒\▒         ▒404       ____/ // / / // /____//  /_/_ /  /_/_
     1▒\▒    *▒0    ▒       /_____//_/ /_//______//______//______/\\
      1▓9▒▒▓# ▒*▓   ÷       \______\_\/\_\\/\\_____\\\\______\\\\______\/
        e▒▒▒▓▒▒  ▓▒▒▒
        
        '''

# anonymous hacker quotes from http://infosecurity24.blogspot.com/p/blog-page_26.html
best_quotes_from_anonymous = [' - Your Ignorance Is Their Power \n   Learn And Unlearn',
                              ' - You Cannot Cut Off That Which Does Not Exist .',
                              ' - Change will not come if we wait for some other person or time. We are the ones We\'ve been waiting for. \n   we are the change that we seek .',
                              ' - Man is least himself when he talks in his own person. Give him a mask and he will tell you the truth.',
                              ' - We are "Anonymous"\n   We do not forgive\n   We do not forget\n   Except us.',
                              ' - People should not be afraid of their Governments. Governments should be afraid of their People.',
                              ' - Nobody can give you freedom \n   nobody can give you equality or justice \n   if you are Man you take it.',
                              ' - But we are hackers and hackers have black terminals with "Green font colors".',
                              ' - Old Hackers never Die. They just go to Bitnet.']

def ping(): # This function is to allow the user to ping a website multiple times to get some info about the connection
    global ui
    ui = ui.lower().split(' ')
    try:
        the_url = ui[1]
    except:
        ping_syntax = '''
    -f : How many times to test connection speed (Default 6)
    -p : Which Specific port to run the website on (Default is... idk lmao)
    -t : Timeout on loading the website (Default is None, idk why but this sometimes does not work)
    -r : Apply when you want to use random headers for connecting (hide your identity)
    '''
        print(ping_syntax)
        return

    ui.pop(0)
    print(f"Pinging \"http://{the_url}\"", end='')
    # po = ping options
    po = {'-f': 6, 
          '-p': '',
          '-t': None, 
          '-r': requests.utils.default_headers()}

    for j in ui:
        if j in po.keys():
            if j != '-r':
                try:
                    po.update({j:int(ui[ui.index(j) + 1])})
                except:
                    print(f'Error: Please enter a number for the port\n[{ui[ui.index(j) + 1]}] is not a valid port number')
                    return
            else:
                ua = UserAgent() # Create the fake user-agent object
                po.update({j:{'User-Agent': f'{ua.random}'}})

    if po['-p'] != '':
        print(f' on port {po["-p"]}', end='')

    if po['-r'] != requests.utils.default_headers():
        print(f'\nUsing Custom Headers:\n{po["-r"]}')
    else:
        print(f'\nUsing default headers')

    print(f"Time taken to request website(seconds): \n")
    try:
        speed_list = []
        for i in range(po['-f']):
            print(f'    Attepmt {i + 1}', end='\r')
            resp = requests.get(f"http://{the_url}:{po['-p']}", timeout=po["-t"], headers=po['-r']).elapsed.total_seconds()
            speed_list.append(resp)
            print(f'''     {resp}''')
        
        print(f'\nAverage Time: {(sum(speed_list) / len(speed_list))} seconds')
            
    except requests.exceptions.ConnectionError:
        print('\nError: Connection Error')
    
    except requests.exceptions.InvalidURL:
        print('\nError: Invalid URL / Invalid Port')
    
    except urllib3.exceptions.LocationParseError:
        print('\nError: URL parsing error')

def echo(): # Print what ever the user inputted
    global ui
    if len(ui) == 4:
        echo_usage = '''
        #   Usage:                   Command:
        1.  echo a message:          echo "information to display"
        2.  write data to a file:    echo "information to write" >> "filename"
        '''
        print(echo_usage)
        return

    ui = ui.replace('echo ','',1)
    ui_list = ui.split(' ')
    if '>>' in ui_list:
        ui = ui.split(' >> ')
        with open(ui[1],'a+') as ff:
            ff.write(ui[0])
            print('Data has been written to file')

    else:
        print(ui)

def cd(): # Changes the working directory of the program
    global ui
    ui = ui.strip(' ').split(' ', 1)
    if len(ui) == 2:
        try:
            if ':' in ui[1]:
                os.chdir(ui[1])
            else:
                os.chdir(os.getcwd() + '\\' + ui[1])
        except:
            print(f'Error: No Such Direcotry:\n{os.getcwd()}\\{ui[1]}\n')
    
    print(f'Current Working Directory:\n{os.getcwd()}')

# How to add new Commands
# add new functions to the shell, write the function name in the "value" of the dictionary named "commands"
# and the keyword the user would use to call the funciton, in the "keys" of the dictionary named "commands"
commands = {
    'ping':ping,
    'echo':echo,
    'cd':cd,
    }

if __name__ == "__main__": # The main process
    try:
        global ui
        ui = 'echo                      Welcome to DedSec Shell' # Display a default message

        while True:
            click.clear() # Clear the console view
            print(skull)

            x = ui.split(' ')[0]
            if x in commands.keys():
                commands[x]()
            else:
                print('Error: Unkown Command')

            ui = input(f'\n\n                           >DEDSEC:/ ')
    except KeyboardInterrupt:
        os._exit(0)