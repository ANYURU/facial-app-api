import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import stdiomask

class mail_alert():
    """
    This class defines the format for sending an email alert to the owner of the system
    """
    def __init__(self):
        self.sen_addr = "egwillface@gmail.com"
        self.rec_addr = "davidderrickanyuru@gmail.com"
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.attach_path = ""
        self.mail_content = """ALERT INTRUDER,
                       There is an unknown person in the premises please take action.
                       Attached is a photo with the intruder's face 
    
                       """
        self.sen_password = ""
        self.mail_subject = "HOME SECURITY. It has an attachment of the intruder's image."

    def set_attach_path(self):
        """This function gets the path of the latest file in its subfolder"""
        files = os.listdir(self.dir_path) 
        paths = [os.path.join(self.dir_path, basename) for basename in files]
        self.attach_path = max(paths, key = os.path.getctime)
        #return(self.attach_path)
        print(self.attach_path)
    
    def set_send_addr(self, addr):
        """This fuction sets the email address of the sender"""
        self.sen_addr = addr
        print("Sender's email address has successfully been updated")

    def set_rec_addr(self, addr):
        """This function sets the receiver's address"""
        self.rec_addr = addr

    def set_mail_content(self, msg):
        """This function modifies the message that the application user wants to send to the receiver"""
        self.mail_content = msg 

    def set_sen_password(self, password):
        """This function sets the sender's password"""
        self.sen_password = password
        print("The user's password has successfully been set")

    def set_mail_subject(self, subject):
        self.mail_subject = subject

    def send_mail(self):
        """This function composes the mail, attaches the file from a directory to the mail and sends it """
        #set up the mime 
        message = MIMEMultipart()
        message['From'] = self.sen_addr
        message['To'] = self.rec_addr
        message['Subject'] = self.mail_subject
        
        #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(self.mail_content, 'plain'))
        attach_file = open(self.attach_path, 'rb')#open the file as binary mode
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) #encode the attachment
        
        #add payload header with filename
        payload.add_header('Content-Decomposition', 'attachment', filename=self.attach_path)
        message.attach(payload)
        
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(self.sen_addr, self.sen_password) #login with mail_id and password
        text = message.as_string()
        session.sendmail(self.sen_addr, self.rec_addr, text)
        session.quit()
        print('Mail Sent')


user = mail_alert()
print("Enter your password\n")
password = stdiomask.getpass()
user.set_sen_password(password)
user.set_attach_path()
user.send_mail()


#print(user.sen_password)
#path = user.get_attach_path()



