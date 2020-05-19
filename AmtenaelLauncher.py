#!/usr/bin/env python3
# coding=utf-8
# Jus de Patate | Aingeth - 2020
# L'objectif est de mimer le comportement du launcher officiel (disponible uniquement sur Windows) de Amtenael
from hashlib import md5
# import de la verification de hash md5
import os
import socket
import json
from platform import system
import threading

try:
    import requests
except ImportError:
    print("Erreur a l'import de requests, Est-il installé ?")
    exit(-1)

try:
    from tkinter import *
    from tkinter import messagebox
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

version = "1.5"

curlheader = {
    'User-Agent': "AmtenaelLauncher-linux/" + version,
}


class AmtenaelLauncher:
    def __init__(self, master):
        self.master = master
        master.title("AmtenaelLauncher "+version)
        master.minsize(200, 350)
        master.resizable(False, False)
        # creation d'une fenetre 200x350 qui ne peut pas changer de taille

        icon_b64 = "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"
        # logo de Amtenael en 256x256 en base64 au format PNG

        icon = PhotoImage(data=icon_b64)
        master.tk.call('wm', 'iconphoto', root._w, icon)
        # maintenant on dit a tkinter que icon_b64 est l'icon de la fenetre

        url = "https://server1.amtenael.fr/json.php"
        connected_json = requests.get(url, headers=curlheader, verify=False)
        # on recupere les informations depuis amtenael avec les meme headers que pour verifier les fichiers
        connected_parsed = json.loads(connected_json.text)
        connected = connected_parsed["account"]["connected"]
        # maintenant on prends le nombre de gens connecté on met dans la variable connected

        self.connected_ppl = StringVar()
        self.connected_ppl.set(connected+" personnages connectés")
        self.connected_ppllabel = Label(master, textvariable=self.connected_ppl)
        # et on met le nombre de gens connecté dans le label qui servai a faire de la place avant :D (ce qui explique son nom)

        self.serveraddr = StringVar()
        self.server = Entry(master, state="disabled", textvariable=self.serveraddr)
        self.serveraddr.set("game.amtenael.fr")
        # creation d'un Entry pour l'addresse du serveur (non changeable mais present)

        self.usernamevar = StringVar()
        self.username = Entry(master, textvariable=self.usernamevar)
        # creation d'un Entry pour le username

        self.passwordvar = StringVar()
        self.password = Entry(master, show="•", textvariable=self.passwordvar)
        # creation d'un Entry pour le password qui n'affiche que des "•"

        if system() == "Linux":
            self.winecfg_button = Button(master, text="winecfg", command=self.winecfg)
            self.fucktkinter99 = Label(master)
        # On ajoute un bouton de configuration Wine si le client utilise Linux
        # system() = platform.system()

        self.connect_button = Button(master, text="Connexion", command=self.connect)
        # bouton de connexion qui appelle la fonction connect()

        self.rememberpasswordvar = BooleanVar()
        self.rememberpassword = Checkbutton(master, text="Mémoriser identifiants ?", var=self.rememberpasswordvar)
        self.rememberpassword.configure(state='normal')
        # Bouton pour savoir si on mémorise le user/mdp

        self.charList = Listbox(master)

        self.connected_ppllabel.pack()
        self.server.place(x=17, y=20)
        self.username.place(x=17, y=60)
        self.password.place(x=17, y=80)
        if system() == "Linux":
            self.winecfg_button.place(x=13, y=110)
            self.connect_button.place(x=93, y=110)
        else:
            self.connect_button.place(x=50, y=110)
        # si l'utilisateur utilise Linux on ajoute un label pour faire de la place, et 2 boutons (connect, winecfg)
        # sinon on pack normalement le bouton connect
        self.rememberpassword.place(x=5, y=140)
        self.charList.place(x=17, y=165)
        # On pack tout

        self.token = "AmtenaelLinux"  # on prépare la variable qui sera modifié pendant preconnect()

        self.checkCreds()  # on verifie que les identifiants ne sont pas sauvegardé
        self.preconnect("login")  # peupler charList avant d'afficher la fenetre
        self.charList.insert(0, "Selection de royaume")  # On ajoute la premiere ligne
        self.password.bind('<Return>', self.preconnect)  # On dit a tkinter que si un utilisateur appuie sur <Return> (entrée), le quicklogin se lance

        threading.Thread(target=self.CheckFiles).start()
        # on vérifie les fichiers du jeu

    def connect(self):
        try:
            charListSelect = self.charList.get(self.charList.curselection())
        except TclError:
            charListSelect = "Selection de royaume"
        # Ici on récupere la selection de l'utilisateur,
        # si il n'a rien selectionné on l'ennemene a la selection de royaume

        if self.username.get() != "" and self.password.get() != "":
            print("Connexion avec", self.username.get(), "sur Amtenael")

            if charListSelect == "Selection de royaume":
                self.startGame("connect.exe game.dll " + self.server.get() + " " + self.username.get() + " " + self.password.get())
            else:
                self.startGame("connect.exe game.dll " + self.server.get() + " " + self.username.get() + " " + self.token + " " + charListSelect)
            # Ici on execute connect.exe soit vers la selection du royaume soit en connexion directe sur un personnage

            if self.rememberpasswordvar.get():
                with open("launcher.dat", "wb") as f:
                    lines = [
                        self.token,
                        self.username.get(),
                        self.password.get()
                    ]
                    for i in lines:
                        f.writelines(i + "\n")
                        i += 1
                    f.close()
        else:
            messagebox.showerror("Erreur", "Veuillez rentrer un nom d'utilisateur et un mot de passe")

    def preconnect(self, event):
        # on est obligé d'indiquer que preconnect() prend un deuxieme argument parce que tkinter donne 2 arguments a
        # chaque fois que l'on appuie sur <return>

        while self.charList.get(1) != "":
            self.charList.delete(END)
        # ici on clean charList pour le re-remplir juste apres

        if self.username.get() != "" and self.password.get() != "":
            nl = "\n"

            try:
                uniqueId=open("/etc/machine-id").read().split("\n")[0]
            except:
                print("Impossible de lire machine-id pour que le serveur identifie le client")
                uniqueId="AmtenaelLauncher-linux\\"+version

            tosend = self.username.get().encode("utf-8") + nl.encode("utf-8") + self.password.get().encode("utf-8") + \
                     nl.encode("utf-8") + uniqueId.encode("utf-8") + nl.encode("utf-8")
            # ici nous preparons la requete a faire au serveur

            # Et maintenant voici l'instant documentation en plein milieu du code du launcher:

            # la requete doit ressembler a ca:
            # {Nom d'utilisateur}\n
            # {Mot de passe}\n
            # {Identifiant Unique}\n (Sur le launcher officiel il est fait d'identifiants de disque dur + CPU, et sur ce launcher, il est constitué du machine id)
            #
            # et la reponse ressemble a ceci:
            # {token} (permet la connection direct a un personnage et remplace le mot de passe dans ce cas)
            # {Nom d'un personnage} {Royaume} (ceci répété pour chaque personnage, {Royaume} est 1, 2 ou 3 pour faciliter la connection avec connect.exe

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.server.get(), 10301))
            s.send(tosend)
            # On envoie au serveur la requete

            char = s.recv(1024).decode().splitlines()
            # on recupere la réponse du serveur, et on la transforme directement en array
            s.close()
            # et on oublie pas de fermer la connection et on va s'en servir pour remplir le widget charList

            if char[0].startswith("error:"):
                messagebox.showwarning("Erreur", "Réponse du serveur:\n"+char[0])
                return False
            # dans le cas ou le serveur nous renvoie une erreur, abandonner ici

            self.token = char[0]  # on a besoin de la premiere ligne pour se connecter plus tard
            if os.path.exists("launcher.dat"):
                with open("launcher.dat", "r") as f:
                    lines = f.read().splitlines()
                    lines[0] = self.token
                    f.close()
                with open("launcher.dat", "w") as f:
                    f.writelines(lines[0]+"\n")
                    for i in lines:
                        f.writelines(i+"\n")
                    f.close()
            else:
                with open("launcher.dat", "w") as f:
                    f.write(self.token)
                    f.close()
            # on lit launcher.dat, si il y a deja du contenu dedans (token\nnom d'utilisateur\nmot de passe)
            # on modifie la premiere ligne (le token) en ajoutant le nouveau token de connexion
            # (un nouveau token par preconnect())

            i = 1  # ignorer la premiere ligne
            while i < len(char):
                self.charList.insert(i, char[i])

                i+=1

    def startGame(self, command):
        if system() == "Windows":
            os.system(command)
        else:
            os.system("wine "+command)
    # si l'utilisateur a Windows, alors executer la commande, sinon utiliser wine pour executer la commande

    def winecfg(self):
        os.system("winecfg")

    def checkCreds(self):
        try:
            with open('launcher.dat') as f:
                lines = f.read().splitlines()
                self.usernamevar.set(lines[1])
                self.passwordvar.set(lines[2])
                print("Mot de passe pour", lines[1], "trouvé")
                self.rememberpassword.toggle()
                f.close()
        except (FileNotFoundError, KeyError, IndexError):
            print("Aucun mot de passe enregistré")

    def CheckFiles(self):
        self.connect_button.config(state="disabled", text="Checking files")
        files = requests.get("https://amtenael.fr/launcher/launcher.txt", headers=curlheader)
        filesstr = files.text
        # maintenant on a le fichier qui nous indique quel fichier verifier

        for i in filesstr.splitlines():
            # je sais que ca pourrais etre plus simple avec une boucle for mais j'aime pas ca ><
            line = i.split(";")

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

                try:
                    with open(filename, "wb") as localfile:
                        localfile.write(newfile.content)
                    # telechargement du nouveau fichier
                except FileNotFoundError:
                    pathtocreate = "./"
                    for folder in filename.split("/")[:-1]:
                        pathtocreate += folder + "/"
                    os.makedirs(pathtocreate)
                    with open(filename, "wb") as localfile:
                        localfile.write(newfile.content)
                    # si on a une erreur de fichier qui n'existe pas on va creer les dossiers et creer le fichier

        self.connect_button.config(state="normal", text="Connexion")


try:
    root = Tk()
    window = AmtenaelLauncher(root)

    root.mainloop()
    # On lance la fenetre
except KeyboardInterrupt:
    exit(0)
except requests.exceptions.SSLError as e:
    print(e)
    messagebox.showerror("Erreur", "Le certificat SSL de la réponse de amtenael.fr n'est pas correct")
except requests.exceptions.HTTPError as e:
    print(e)
    messagebox.showerror("Erreur", "AmtenaelLauncher a reçu un code de réponse HTTP invalide")
    exit(-1)
except requests.exceptions.ConnectionError as e:
    print(e)
    messagebox.showerror("Erreur", "AmtenaelLauncher n'a pas été capable de recuperer les fichiers depuis amtenael.fr")
    exit(-1)
except IOError as e:
    print(e)
    messagebox.showerror("Erreur", "AmtenaelLauncher n'a pas été capable d'écrire ou de lire sur le disque dur")
