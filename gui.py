from tkinter import messagebox, Tk, LabelFrame, Label, Button, Entry, Spinbox, Text, END
from email_extractor import EmailException, EmailWarning
from signature_remover import SignatureRemover
from classifier import ClassifierException

class GUI():

    def __init__(self):
        self.root = Tk(className='Программа для удаление подписей из электронных писем')
        self.root.geometry("1000x600")
        self.root.wm_resizable(False, False)

        self.panelFrame = LabelFrame(self.root, height = 100, text="")
        self.panelFrame.pack(side = 'top', fill = 'x')
        
        self.labelLogin = Label(self.panelFrame, text="Адрес почты: ")
        self.labelLogin.place(x=10, y=40)

        self.loginField = Entry(self.panelFrame, width=20)
        self.loginField.place(x=100, y=40)

        self.labelPassword = Label(self.panelFrame, text="Пароль: ")
        self.labelPassword.place(x=280, y=40)

        self.passwordField = Entry(self.panelFrame, show="*", width=15)
        self.passwordField.place(x=340, y=40)

        self.labelLogin = Label(self.panelFrame, text="Порядковый номер письма \nв папке 'входящие': ")
        self.labelLogin.place(x=490, y=30)
        
        self.sb = Spinbox(self.panelFrame, from_=1, to=10000)
        self.sb.place(x=690, y=40, width=50)

        self.buttonDeleteSing = Button(self.panelFrame, text="Удалить подпись",
                                        command=self._delete_signature)
        self.buttonDeleteSing.place(x=770, y=15, width=200)

        self.buttonInfo = Button(self.panelFrame, text="Помощь")
        self.buttonInfo.place(x=770, y=45, width=200)

        self.buttonInfo.bind('<ButtonRelease-1>', GUI._show_info)

        self.textFrame1 = LabelFrame(self.root, width=500, text='Исходный текст письма')
        self.textFrame1.pack(fill='y', side='left')

        self.textbox1 = Text(self.textFrame1, font='Arial 12', wrap='word')
        self.textbox1.pack(side = 'left', fill='both')
        self.textbox1.place(width=490)

        self.textFrame2 = LabelFrame(self.root, width=500, text='Текст без подписи')
        self.textFrame2.pack(fill='y', side='right')

        self.textbox2 = Text(self.textFrame2, font='Arial 12', wrap='word')
        self.textbox2.pack(side = 'left', fill='both')
        self.textbox2.place(width=490)


    def _show_messagebox(self, messageType, message):
        if messageType == 'error':
            messagebox.showerror('Ошибка', message)
        elif messageType == 'warning':
            messagebox.showwarning('Предупреждение', message)
        else:
            messagebox.showinfo('Info', message)

    def _delete_signature(self):
        
        address = self.loginField.get()
        password = self.passwordField.get()
        index = int(self.sb.get())

        try:
           original, without_sign =  SignatureRemover.delete_signature(address, password, index)
        except EmailException as e:
            self._show_messagebox('error', str(e))
            return
        except EmailWarning as e:
            self._show_messagebox('warning', str(e))
            return
        except ClassifierException as e:
            self._show_messagebox('error', "Ошибка при загрузке классификатора:\n" + str(e))
            return

        self._show_email_lines(original, self.textbox1)
        self._show_email_lines(without_sign, self.textbox2)

        del_lines_count = len(original) - len(without_sign)

        self._show_messagebox('info', "Удалено строк: " + str(del_lines_count))

    def _show_info(self):
        messagebox.showinfo('Информация', 'Программа позволяет удалять подпись '
        'из текстов электронных писем папки "Входящие" почтового ящика gmail.\nУдаление ' 
        'подписи возможно в письмах, содержащих только текст.'
        '\nДля удаления подписи из письма введите адрес электронной почты, пароль и порядковый номер'
        ' письма в папке "Входящие", затем нажмите кнопку "Удалить подпись"')


    def _show_email_lines(self, lines, textbox):
        textbox.delete('1.0', END)
        all_lines = "\n".join(lines)
        textbox.insert('1.0', all_lines)

    def show(self):
        self.root.mainloop()

    