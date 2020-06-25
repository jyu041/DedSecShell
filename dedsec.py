# Most of these modules are included when you install python
import threading, time, os, click, random, shutil

# Thes modules require a pip install
from fake_useragent import UserAgent
import requests, urllib3, shlex

ui = 'echo                      Welcome to DedSec Shell' # Display a default message

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

def _ping(): # This function is to allow the user to ping a website multiple times to get some info about the connection
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

def _echo(): # Print what ever the user inputted
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
            ff.write(f'{ui[0]}\n')
            print('Data has been written to file')

    else:
        print(ui)

def _cd(): # Changes the working directory of the program
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

def _help():
    help_data = f'''
    Welcome to Dedsec Shell, This is a terminal coded in python to emulate 
    some features of various shells and terminals from different systems.
    It is an incomplete and always improving "shell". The name is called 
    Dedsec Shell because it's theme was inspired by the hacking video game
    named "watch_dogs" by Ubisoft.
    '''
    print(help_data)
    print('#.   Command:        Usage;')
    for indx, possible_cmd in enumerate(commands.keys()):
        print(f'{indx + 1}.{" " * (4 - len(str(indx + 1)))}{possible_cmd}{" " * (16 - len(possible_cmd))}{commands[possible_cmd][1]}')

def _mkdir():
    global ui
    ui = ui.strip(' ').replace('mkdir ','',1)

    if ui == 'mkdir':
        print('You need to enter a name for a directory!')

    elif os.path.isdir(f'{ui}') == True:
        print('This directory already exists, cannot create it again!')

    else:
        os.mkdir(ui)
        print('Created directory')

def _rm():
    global ui
    ui = ui.strip(' ').replace('rm ','',1)
    rm_syntax = '''
    The command : "rm" is a power to remove files and directories
    to recursively remove a directory, add "-r" to the command like this:
    rm [directory to delete] -r

    Basic Usage:
    rm [file/directory to remove]
    '''
    if ui == 'rm':
        print(rm_syntax)
    else:
        temp = shlex.split(ui)
        if os.path.isdir(temp[0]) == True:
            if '-r' in temp:
                shutil.rmtree(temp[0])
            else:
                try:
                    os.rmdir(temp[0])
                except:
                    print(f'Directory [{temp[0]}] is not empty!')
                    return
        else:
            try:
                os.unlink(temp[0])
            except FileNotFoundError:
                print('No such file or folder found!')
                return

        print(f'Successfully removed "{temp[0]}"')

def _ls():
    all_files = os.listdir()
    # This function below is to convert bytes into bigger and easier to read units
    def human(size):
        B = " B"
        KB = "KB" 
        MB = "MB"
        GB = "GB"
        TB = "TB"
        UNITS = [B, KB, MB, GB, TB]
        HUMANFMT = '%f %s %s'
        HUMANRADIX = 1024.
        for u in UNITS[:-1]:
            if size < HUMANRADIX : return HUMANFMT % (size, " " * (18 - (len(str(size).split('.')[0]) + 7)), u)
            size /= HUMANRADIX

        return HUMANFMT % (size, " " * (18 - (len(str(size).split('.')[0]) + 7)), UNITS[-1])
    # C:\Users\jerry\Desktop
    print('        Size:' + " " * 12 + "Unit:" + " " * 18 + 'Name:')
    for i_file in all_files:
        r_size = str(human(os.lstat(i_file).st_size))
        f_size = r_size + " " * (40 - len(str(r_size)))
        if len('<DIR>   ' + f_size + i_file) > 90:
            if os.path.isdir(i_file) == True:
                print(str('<DIR>   ' + f_size + i_file)[:90] + '...')
            else:
                print(str('        ' + f_size + i_file)[:90] + '...')
        else:
            if os.path.isdir(i_file) == True:
                print('<DIR>   ' + f_size + i_file)
            else:
                print('        ' + f_size + i_file)

def _cp():
    global ui
    ui = ui.strip(' ').replace('cp ','',1)
    if ui == 'cp':
        print('You need to enter a directory name or file name!')
    else:
        ui = shlex.split(ui)
        try:
            src = ui[0].strip(' ').strip('"')
            dst = ui[1].strip(' ').strip('"')
        except:
            print('Please enter the command correctly!')

        else:
            try:
                print(f'Starting: Copying [{src}] to [{dst}]')
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy(src, dst)

                print(f'Finished: Copied  [{src}] to [{dst}]')
            except Exception as e:
                print(f'Fatal Error: {e}')

def _mv():
    print('Current Function not yet developed')

# How to add new Commands:
# add new functions to the shell, write the function name in the "value" of the dictionary named "commands"
# and the keyword the user would use to call the funciton, in the "keys" of the dictionary named "commands"
# Please add a description in the second spot for the list of values"
commands = {
    'ping': [_ping,   'Ping an IP for the request time'],
    'echo': [_echo,   'Print a message the user enters or write data to a file'],
    'cd':   [_cd,     'Changes working directory or display current directory'],
    'help': [_help,   'Display this message'],
    'mkdir':[_mkdir,  'Create a directory/folder with name of user input'],
    'rm':   [_rm,     'Remove a file or a directory'],
    'ls':   [_ls,     'List all files in current working directory'],
    'cp':   [_cp,     'Copy a file or a directory to a target location'],
    'mv':   [_mv,     'Move a file from one place to another']
    }

def input_checker():
    global ui
    long_ui = ui.split(' && ')

    for one_ui in long_ui:
        ui = one_ui
        x = ui.split(' ')[0]
        if x in commands.keys():
            commands[x][0]()
        else:
            if len(ui) == 0:
                print(random.choice(best_quotes_from_anonymous))
            else:
                print('Error: Unkown Command')

if __name__ == "__main__": # The main process
    try:
        while True:
            click.clear() # Clear the console view
            print(skull)  # Prints the cool title screen thing
            input_checker()
            ui = input(f'\n\n                           >DEDSEC:/ ')
    except KeyboardInterrupt:
        os._exit(0)