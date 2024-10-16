import tkinter as tk
from tkinter import ttk
import presentation.util.encoding_decoding as end_dec
from tkinter import ttk, messagebox
from tkinter.font import BOLD
from presentation.formularios.form_maestro_design import FormMaestro
from presentation.formularios.form_login_design import FormLoginDesign
from presentation.formularios.form_register import FormRegister
from db.repository.auth_user_repository import AuthUserRepositroy
from db.model import Auth_User

class FormLogin(FormLoginDesign):

    def __init__(self):
        self.auth_repository = AuthUserRepositroy()
        super().__init__()

    def verificar(self):
        user_db: Auth_User = self.auth_repository.getUserByUserName(
            self.usuario.get())
        if(self.isUser(user_db)):
            self.isPassword(self.password.get(), user_db)

    def userRegister(self):
        FormRegister()

    def isUser(self, user: Auth_User):
        status: bool = True
        if(user == None):
            status = False
            messagebox.showerror(
                message="El usuario no existe por favor registrese", title="Mensaje",parent=self.ventana)            
        return status

    def isPassword(self, password: str, user: Auth_User):
        b_password = end_dec.decrypt(user.password)
        if(password == b_password):
            self.ventana.destroy()
            FormMaestro()
        else:
            messagebox.showerror(
                message="La contraseña no es correcta", title="Mensaje")