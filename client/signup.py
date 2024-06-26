import customtkinter as ctk
import ldap
import hashlib
import tkinter.messagebox as tkmb
from CA_client import certif_handling
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#app = ctk.CTk()
#app.geometry("600x600")
#app.title("TekupLive Registration")

LDAP_BASE_DN = "ou=users,dc=tekuplive"

def register(numC_entry,nom_entry,prenom_entry,email_entry,login_entry,genre_entry,pwd_entry):
    numC = numC_entry.get()
    nom = nom_entry.get()
    prenom = prenom_entry.get()
    email = email_entry.get()
    login = login_entry.get()
    genre = genre_entry.get()
    pwd = pwd_entry.get()

    dn = 'cn=' + login + ',' + LDAP_BASE_DN
    hashed_pwd = hashlib.sha256(pwd.encode("UTF-8")).hexdigest()
    entry = [
        ('objectClass', [b'top', b'person', b'organizationalPerson', b'inetOrgPerson']),
        ('uid', numC.encode("UTF-8")),
        ('givenname', nom.encode("UTF-8")),
        ('sn', prenom.encode("UTF-8")),
        ('mail', email.encode("UTF-8")),
        ('cn', login.encode("UTF-8")),
        ("title", genre.encode("UTF-8")),
        ('userPassword', hashed_pwd.encode("UTF-8"))]

    ldap_conn = ldap.initialize("ldap://172.0.0.1:389")
    ldap_conn.protocol_version = ldap.VERSION3
    ldap_conn.simple_bind_s("cn=admin,dc=tekuplive", "admin")

    try:
        ldap_conn.add_s(dn, entry)
        tkmb.showinfo("Registration Success", "User registered successfully!")
    except Exception as e:
        tkmb.showerror("Registration Error", f"Error: {e}")
    finally:
        ldap_conn.unbind_s()
    certif_handling(login)


def swaptologin(fra,fre):
    fra.pack(fill='both',expand=1)
    fre.forget()


def swapsignup(app,fra):
    fra.forget()

    frame = ctk.CTkFrame(master=app)
    frame.pack(pady=20, padx=40, fill='both', expand=1)

    label = ctk.CTkLabel(frame, text="TekupLive Registration")
    label.pack(pady=20)
    numC_entry = ctk.CTkEntry(master=frame, placeholder_text="Num carte")
    numC_entry.pack(pady=12, padx=10)

    nom_entry = ctk.CTkEntry(master=frame, placeholder_text="nom")
    nom_entry.pack(pady=12, padx=10)

    prenom_entry = ctk.CTkEntry(master=frame, placeholder_text="prenom")
    prenom_entry.pack(pady=12, padx=10)

    email_entry = ctk.CTkEntry(master=frame, placeholder_text="Email")
    email_entry.pack(pady=12, padx=10)

    login_entry = ctk.CTkEntry(master=frame, placeholder_text="Login")
    login_entry.pack(pady=12, padx=10)

    genre_entry = ctk.CTkEntry(master=frame, placeholder_text="genre")
    genre_entry.pack(pady=12, padx=10)

    pwd_entry = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
    pwd_entry.pack(pady=12, padx=10)

    register_button = ctk.CTkButton(master=frame, text='Signup', command= lambda:register(numC_entry,nom_entry,prenom_entry,email_entry,login_entry,genre_entry,pwd_entry))
    register_button.pack(pady=12, padx=10)

    gotologin = ctk.CTkButton(master=frame, text='login', command= lambda : swaptologin(fra,frame))
    gotologin.pack(pady=12, padx=10)
#app.mainloop()
