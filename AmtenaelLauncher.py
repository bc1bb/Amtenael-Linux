#!/usr/bin/env python3
# Jus de Patate | Aingeth - 2020
# L'objectif est de mimer le comportement de Patcher.exe, le launcher Windows de Amtenael
from hashlib import md5
# import de la verification de hash md5
import os
import socket

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

version = "1.3"


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
        # creation d'un Entry pour l'addresse du serveur (non changeable mais present dans le cas d'un fork (TODO))

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

        # self.rememberpasswordvar = IntVar()
        # self.rememberpassword = Checkbutton(master, text="Se souvenir des identifiants ?", var=self.rememberpasswordvar)
        # self.rememberpassword.configure(state='normal')
        # Bouton pour savoir si on mémorise le user/mdp
        # les checkbutton ne fonctionnent pas sur ma machine de test, cette fonctionnalité attendra (désolé :p) TODO

        self.charList = Listbox(master)

        self.fucktkinterlol.pack()
        self.server.pack()
        self.fucktkinter0.pack()
        self.username.pack()
        self.fucktkinter.pack()
        self.password.pack()
        self.fucktkinter2.pack()
        self.connect_button.pack()
        # self.rememberpassword.pack()
        self.charList.pack()
        # On pack tout

        self.token = "AmtenaelLinux"  # on prépare la variable qui sera modifié pendant preconnect()

        self.checkCreds()  # on verifie que les identifiants ne sont pas sauvegardé
        self.preconnect()  # peupler charList avant d'afficher la fenetre
        self.charList.insert(0, "Selection de royaume")  # On ajoute la premiere ligne

    def connect(self):
        try:
            charListSelect = self.charList.get(self.charList.curselection())
        except TclError:
            charListSelect = "Selection de royaume"
        # Ici on récupere la selection de l'utilisateur, si il n'a rien selectionné on l'ennemene a la selection de royaume

        if self.username.get() != "" and self.password.get() != "":
            print("Connexion avec", self.username.get(), "sur Amtenael")

            if charListSelect == "Selection de royaume":
                os.system("wine connect.exe game.dll " + self.server.get() + " " + self.username.get() + " " + self.password.get())
            else:
                os.system("wine connect.exe game.dll " + self.server.get() + " " + self.username.get() + " " + self.token + " " + charListSelect)
            # Ici on execute connect.exe (avec wine) sois vers la selection du royaume soit en connexion directe sur un personnage

            # if self.rememberpasswordvar.get() == 1:
            #     with open("launcher.dat", "a") as f:
            #         f.write("AmtenaelLauncher-linux\n"+self.username.get()+"\n"+self.password.get()+"\n")
            #         # sauvegarder les identifiants
            #         f.close()
        else:
            messagebox.showerror("Erreur", "Veuillez rentrer un nom d'utilisateur et un mot de passe")

    def preconnect(self):
        if self.username.get() != "" and self.password.get() != "":
            nl = "\n"
            uniqueId="AmtenaelLauncher-linux\\"+version
            tosend = self.username.get().encode("utf-8") + nl.encode("utf-8") + self.password.get().encode("utf-8") + \
                     nl.encode("utf-8") + uniqueId.encode("utf-8") + nl.encode("utf-8")
            # ici nous preparons la requete a faire au serveur

            # Et maintenant voici l'instant documentation en plein milieu du code du launcher:

            # la requete doit ressembler a ca:
            # {Nom d'utilisateur}\n
            # {Mot de passe}\n
            # {Identifiant Unique}\n (sur windows il est constitué de l'identifiant du processeur+identifiant du disque dur)
            #
            # et la reponse ressemble a ceci:
            # {token} (permet la connection direct a un personnage et remplace le mot de passe dans ce cas)
            # {Nom d'un personnage} {Royaume} (ceci répété pour chaque personnage, {Royaume} est 1, 2 ou 3 pour faciliter la connection avec connect.exe

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.server.get(), 10301))
            s.send(tosend)
            # On envoie au serveur la requete

            char = s.recv(1024).decode().splitlines()
            # on recupere la réponse du serveur, et on la transforme directement en string
            s.close()
            # et on oublie pas de fermer la connection et on va s'en servir pour remplir le widget charList

            self.token = char[0]  # on a besoin de la premiere ligne pour se connecter plus tard
            i = 1  # ignorer la premiere ligne
            while i < len(char):
                self.charList.insert(i, char[i])

                i+=1

    def checkCreds(self):
        try:
            with open('launcher.dat') as f:
                lines = f.read().splitlines()
                self.usernamevar.set(lines[1])
                self.passwordvar.set(lines[2])
                print("Mot de passe pour", lines[1], "trouvé")
                # self.rememberpassword.toggle()
                f.close()
        except FileNotFoundError or KeyError:
            print("Aucun mot de passe enregistré")


try:
    root = Tk()
    window = AmtenaelLauncher(root)

    CheckFiles()
    # On vérifie les fichiers avant d'afficher le launcher

    root.mainloop()
    # On lance la fenetre
except KeyboardInterrupt:
    exit(0)
except requests.exceptions.SSLError as e:
    print(e)
    messagebox.showerror("Erreur", "Le certificat SSL de la réponse de amtenael.fr n'est pas correct, changez la variable SSLImportant au début du fichier pour ne pas vérifier le certificat")
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
    messagebox.showerror("Erreur", "AmtenaelLauncher n'a pas été capapble d'écrire ou de lire sur le disque dur")
