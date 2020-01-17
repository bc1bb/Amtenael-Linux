#!/usr/bin/env python3
# Jus de Patate | Aingeth - 2020
# L'objectif est de mimer le comportement de Patcher.exe, le launcher Windows de Amtenael
from hashlib import md5
# import de la verification de hash md5
import os

try:
    import requests
except ImportError:
    print("Erreur a l'import de requests, Est-il installé ?")
    exit(-1)

try:
    from tkinter import *
    # import de tkinter pour faire des fenetres
except ImportError:
    print("Erreur a l'import de tkinter, Est-il installé ? Utilisez-vous Python 3.x ?")
    exit(-1)

try:
    open("game.dll").close()
    # On essaie d'ouvrir le fichier game.dll et de le refermer pour voir si il existe (installation valide ou pas)
except FileNotFoundError:
    print("On dirait que AmtenaelLauncher n'est pas dans un dossier avec une installation valide de Dark Age of Camelot")
    exit(-1)

version = "1.2"


class CheckFiles:
    def __init__(self):
        headers = {
            'User-Agent': "AmtenaelLauncher-linux/" + version,
        }

        files = requests.get("https://amtenael.fr/launcher/launcher.txt", headers=headers)
        filesstr = files.text
        # maintenant on a le fichier qui nous indique quel fichier verifier

        i = 0
        while i < len(filesstr.splitlines()):
            # je sais que ca pourrais etre plus simple avec une boucle for mais j'aime pas ca ><
            line = filesstr.splitlines()[i].split(";")

            filename = line[0]
            url = line[1]
            hash = line[2]

            try:
                localhash = md5(open(filename, "rb").read()).hexdigest()
            except FileNotFoundError:
                localhash = 0
                # dans le cas ou le fichier n'existe pas, on met le hash a une valeur de merde
                # pour faire rater le check dans tous les cas

            if hash == localhash:
                print(filename, "est correct")
                # debug mais on va y laisser la :p
            else:
                print(filename, "n'est pas correct, téléchargement en cours...")
                newfile = requests.get(url)

                with open(filename, "wb") as localfile:
                    localfile.write(newfile.content)
                    # telechargement du nouveau fichier

            i += 1


class AmtenaelLauncher:
    def __init__(self, master):
        self.master = master
        master.title("AmtenaelLauncher "+version)
        master.minsize(200, 350)
        master.resizable(False, False)
        # creation d'une fenetre 200x350 qui ne peut pas changer de taille

        self.fucktkinterlol = Label(master)
        # pour faire de la place

        self.serveraddr = StringVar()
        self.server = Entry(master, state="disabled", textvariable=self.serveraddr)
        self.serveraddr.set("game.amtenael.fr")
        # creation d'un Entry pour l'addresse du serveur (non changeable mais present)

        self.fucktkinter0 = Label(master)
        # pour faire de la place

        self.usernamevar = StringVar()
        self.username = Entry(master, textvariable=self.usernamevar)
        # creation d'un Entry pour le username

        self.fucktkinter = Label(master, text="")
        # pour faire de la place

        self.passwordvar = StringVar()
        self.password = Entry(master, show="•", textvariable=self.passwordvar)
        # creation d'un Entry pour le password qui n'affiche que des "•"

        self.fucktkinter2 = Label(master, text="")
        # pour faire de la place

        self.connect_button = Button(master, text="Connexion", command=self.connect)
        # bouton de connexion qui appelle la fonction connect()

        self.rememberpasswordvar = IntVar()
        self.rememberpassword = Checkbutton(master, text="Se souvenir des identifiants ?", var=self.rememberpasswordvar)
        # Bouton pour savoir si on mémorise le user/mdp

        self.fucktkinterlol.pack()
        self.server.pack()
        self.fucktkinter0.pack()
        self.username.pack()
        self.fucktkinter.pack()
        self.password.pack()
        self.fucktkinter2.pack()
        self.connect_button.pack()
        # On pack tout

        self.checkCreds()

    def connect(self):
        print("Connexion avec", self.username.get(), "sur Amtenael")
        os.system("wine connect.exe game.dll "+self.server.get()+" "+self.username.get()+" "+self.password.get())


    def checkCreds(self):
        try:
            with open('launcher.dat') as f:
                lines = f.read().splitlines()
                self.usernamevar.set(lines[1])
                self.passwordvar.set(lines[2])
                print("Mot de passe pour", lines[1], "trouvé")
                self.rememberpassword.toggle()
                f.close()
        except FileNotFoundError or KeyError:
            print("Aucun mot de passe enregistré")
try:
    CheckFiles()
    # Verifions les fichiers avant d'afficher le launcher

    root = Tk()
    window = AmtenaelLauncher(root)
    root.mainloop()
    # On lance la fenetre
except KeyboardInterrupt:
    exit(0)
