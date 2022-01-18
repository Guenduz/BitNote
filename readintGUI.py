import sys
from PyQt5 import QtCore, QtWidgets
import sys
import json
import datetime
from time import sleep
from cryptography.fernet import Fernet
import base64
import hashlib
maintext = '''
            {
                "Note_data": [
                ],
                "User": [
                ]
            }
            '''
try:
    with open("data.json","x") as file:
        with open("data.json","w") as file_:
            file_.write(maintext)
except:
    with open("data.json","r+") as file:
        check=file.read().strip()
        if check=="":
            file.write(maintext)


class MainWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str,str)

    def __init__(self,Name,Password):
        self.Name=Name
        self.Password=Password
        QtWidgets.QWidget.__init__(self)
        self.setObjectName("Form")
        self.resize(552, 350)
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(10, 20, 191, 321))
        self.listWidget.setObjectName("listWidget")


        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(450, 5, 100, 20))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("AddNote")
        self.pushButton.clicked.connect(self.switch)

        self.load_titels()

        self.label_1 = QtWidgets.QTextBrowser(self)
        self.label_1.setGeometry(QtCore.QRect(220, 110, 321, 231))
        self.label_1.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(230, 80, 291, 19))
        self.label.setObjectName("label")
        self.label.setText("Title")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(230, 30, 291, 19))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Date")

        self.listWidget.itemDoubleClicked.connect(self.getItem)

        QtCore.QMetaObject.connectSlotsByName(self)
   
    def load_titels(self):
        user_pass=str(self.Password)
        key=user_pass+str("B"*(32-len(user_pass)))
        key=base64.b64encode(key.encode("utf-8"))
        crypter=Fernet(key)
       
        with open("data.json","r") as f:
            json_data=json.loads(f.read())
            x=0
            check=0
            while check!=-1:
                try:
                    if str(json_data["Note_data"][x]["name"])==str(self.Name):
                        data=json_data["Note_data"][x]["title"]
                        data=data.encode('UTF-8')
                        decryptstring=crypter.decrypt(data)
                        data=str(decryptstring,'utf8')
                        self.listWidget.insertItem(x,data)

                except IndexError:
                    check=-1
                if check!=-1:
                    x+=1

    def getItem(self):
        x=self.listWidget.currentRow()
        title_=str(self.listWidget.currentItem().text())
        x=0
        user_pass=str(self.Password)
        key=user_pass+str("B"*(32-len(user_pass)))
        key=base64.b64encode(key.encode("utf-8"))
        crypter=Fernet(key)

        with open("data.json","r") as f:
            json_data=json.loads(f.read())
            while True:
                try:
                    encoded_title=json_data["Note_data"][x]["title"].encode('UTF-8')
                except IndexError:
                    x=x-1
                    break
                try:
                    encoded_title=crypter.decrypt(encoded_title)
                    encoded_title=str(encoded_title,'utf8')
                except:
                    pass
                if encoded_title==title_:
                    break
                x+=1

        with open("data.json","r") as f:
            json_data=json.loads(f.read())
            try:
                data=json_data["Note_data"][x]["text"]
                data=data.encode('UTF-8')
                decryptstring=crypter.decrypt(data)
                data=str(decryptstring,'utf8')
            except:
                data=str("This_Is_A_Problem")

        self.label.setText(json_data["Note_data"][x]["date"])
        self.label_2.setText(self.listWidget.currentItem().text())
        self.label_1.setText(data)

    def switch(self):
        self.switch_window.emit(self.Name,self.Password)

class Login(QtWidgets.QWidget):

    switch_window_main = QtCore.pyqtSignal(str,str)
    switch_window_register = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setObjectName("Form")
        self.resize(400, 300)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(90, 50, 191, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 110, 191, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(140, 170, 96, 35))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Login")
        self.pushButton.clicked.connect(self.LogIn)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 260, 96, 35))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Register")
        self.pushButton_2.clicked.connect(self.GoRegister)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 30, 61, 20))
        self.label.setObjectName("label")
        self.label.setText("Name")

        self.label_1= QtWidgets.QLabel(self)
        self.label_1.setGeometry(QtCore.QRect(250, 260, 120, 35))
        self.label_1.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Password")
        QtCore.QMetaObject.connectSlotsByName(self)

    def LogIn(self):
        x=0
        Name=self.lineEdit.text()
        Password=self.lineEdit_2.text()            
        md5 = hashlib.md5(Password.encode('UTF-8'))
        Password=str(md5.hexdigest())
        
        with open("data.json","r") as f:
            json_data=json.loads(f.read())
            while x!=-1:
                try:
                    if json_data["User"][x]["Username"]==Name:
                        StoredName=json_data["User"][x]["Username"]
                        storedPass=json_data["User"][x]["Password"]
                        if storedPass==Password:
                            self.GoMain()
                        else:
                            self.lineEdit.clear
                            self.lineEdit_2.clear
                            self.label_1.setText("Wrong Password")
                        x=-1
                except IndexError:
                    self.label_1.setText("User Not Found")
                    x=-1

                if x!=-1:
                    x+=1

    def GoMain(self):
        self.switch_window_main.emit(self.lineEdit.text(),self.lineEdit_2.text())
    def GoRegister(self):
        self.switch_window_register.emit()

class Register(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setObjectName("Form")
        self.resize(400, 300)

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(150, 30, 171, 33))
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_1 = QtWidgets.QLabel(self)
        self.lineEdit_1.setGeometry(QtCore.QRect(250, 260, 120, 35))
        self.lineEdit_1.setObjectName("Lable_1")

        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(150, 90, 171, 33))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(150, 150, 171, 33))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(180, 200, 96, 35))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Register")

        self.pushButton.clicked.connect(self.Save_User_info)
        
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 264, 91, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Login")
        self.pushButton_2.clicked.connect(self.login)


        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 10, 67, 19))
        self.label.setObjectName("label")
        self.label.setText("Name")

        
        self.label_1= QtWidgets.QLabel(self)
        self.label_1.setGeometry(QtCore.QRect(250, 260, 120, 35))
        self.label_1.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 67, 19))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Passord")
        
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 131, 19))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("RetypePassword")

        QtCore.QMetaObject.connectSlotsByName(self)

    def Save_User_info(self):
        check=0
        Name=self.lineEdit.text()
        with open("data.json","r") as f:
            json_data=json.loads(f.read())

            while True:
                try:
                    if json_data["User"][check]["Username"]==Name:
                        check=-1
                        break
                except IndexError:
                    check=0
                    break
                check+=1
        if check==0:    
            if self.lineEdit_2.text()==self.lineEdit_3.text() and self.lineEdit_2.text().strip()!="":
                Password=self.lineEdit_2.text()            
                md5 = hashlib.md5(Password.encode('UTF-8'))
                Password=str(md5.hexdigest())

                dictt={
                    "Username" : Name,
                    "Password" : Password,
                    }

                with open("data.json","r+") as file:
                    file_data=json.load(file)
                    file_data["User"].append(dictt)
                    file.seek(0)
                    json.dump(file_data,file,indent=4)
                self.lineEdit.clear()
                self.lineEdit_2.clear()
                self.lineEdit_3.clear()
                self.lineEdit_1.setText("User Created")
           
            else:
                self.lineEdit.clear()
                self.lineEdit_2.clear()
                self.lineEdit_3.clear()
                self.lineEdit_1.setText("Password not match")

        else:
            self.lineEdit_1.setText("This Name is Taken")
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()

    def login(self):
        self.switch_window.emit()


class AddNote(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str,str)

    def __init__(self,Name,Password):
        self.Name=Name
        self.Password=Password
        QtWidgets.QWidget.__init__(self)
        self.setObjectName("Form")
        self.resize(577, 476)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(230, 420, 101, 41))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Save")

        self.pushButton1 = QtWidgets.QPushButton(self)
        self.pushButton1.setGeometry(QtCore.QRect(450, 5, 100, 20))
        self.pushButton1.setObjectName("pushButton")
        self.pushButton1.setText("ReadNotes")
        self.pushButton1.clicked.connect(self.GoRead)
 
        self.save=QtWidgets.QLabel(self)
        self.save.setGeometry(QtCore.QRect(20, 420, 101, 50))
        self.plainTextEdit = QtWidgets.QTextEdit(self)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 110, 551, 301))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(30, 30, 113, 33))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 10, 67, 19))
        self.label.setObjectName("label")
        self.label.setText("Title")

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 67, 19))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Text")

        self.pushButton.clicked.connect(lambda:self.print_shit(self.lineEdit,self.plainTextEdit,self.save))

        QtCore.QMetaObject.connectSlotsByName(self)


    def print_shit(self,lineEdit,plainTextEdit,save):
    #get the data from guis
        user_pass=str(self.Password)
        title=lineEdit.text()
        text=plainTextEdit.toPlainText()
        #check if the data!=NULL
        if title.strip()!="" and text.strip()!="":
            #creating the encyption key
            key=user_pass+str("B"*(32-len(user_pass)))
            key=base64.b64encode(key.encode("utf-8"))
            crypter=Fernet(key)
            #encypting data
            title=str(crypter.encrypt(title.encode('UTF-8')),'utf8')
            text=str(crypter.encrypt(text.encode('UTF-8')),'utf8')
            #get the time
            dt = datetime.datetime.now()
            time=dt.strftime('%Y/%m/%d %H:%M:%S %A')
            #the form of the data that will be in the json file
            main_text='''
            {
                "Note_data": [
                ],
                "User": [
                ]
            }
            '''
            #form of data to save
            dictt={
                "title" : title,
                "text" : text,
                "date" : str(time),
                "name" : self.Name
                }
            #opening the file
            with open("data.json","r+") as file:
                #if the file has the form append the data "dictt"
                try:

                    file_data=json.load(file)
                    file_data["Note_data"].append(dictt)
                    file.seek(0)
                    json.dump(file_data,file,indent=4)
                #if not enter the data form in the json file and enter the data "dictt"
                except:
                    file.write(main_text)
                    file_data=json.load(file)
                    file_data["Note_data"].append(dictt)
                    file.seek(0)
                    json.dump(file_data,file,indent=4)
            #if the data is saved"maybe"print saved in the gui
            save.setText("Saved")
            lineEdit.clear()
            plainTextEdit.clear()
        #if there is no data print error in the gui
        else:
            save.setText("Error")


    def GoRead(self):
        self.switch_window.emit(self.Name,self.Password)

class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = Login()
        self.login.switch_window_main.connect(self.show_main)
        self.login.switch_window_register.connect(self.show_register)
        try:
            self.register_window.close()
        except:
            pass 
        self.login.show()

    def show_main(self,Name,Password):
        self.main_window = MainWindow(Name,Password)
        self.main_window.switch_window.connect(self.show_add_note)
        self.login.close()
        try:
            self.Note_window.close()
        except:
            pass
        self.main_window.show()
    
    def show_add_note(self,Name,Password):
        self.Note_window=AddNote(Name,Password)
        self.Note_window.switch_window.connect(self.show_main)
        self.main_window.close()
        self.Note_window.show()

    def show_register(self):
        self.register_window=Register()
        self.register_window.switch_window.connect(self.show_login)
        self.login.close()
        self.register_window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()