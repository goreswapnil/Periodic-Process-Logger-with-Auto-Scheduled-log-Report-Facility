from sys import*
import psutil
import  smtplib
import urllib.request
import os
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email.mime.multipart import MIMEMultipart

def is_connected():
    try:
        urllib.request.urlopen('http://216.58.192.142',timeout=6)
        return True
    except urllib.request.URLError:
        return False

def MailSender(gmail_user,gamil_password,filename,mail_dest):
    sent_from = gmail_user
    to = mail_dest

    try:
        msg = MIMEMultipart()
        Subject = """Information about running Process"""
        msg['Subject'] = Subject 
        attachment = open(filename,"rb")
        p = MIMEBase('application','octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition',"attachment; filename=%s"%filename)
        msg.attach(p)

        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.ehlo()
        server.login(gmail_user,gamil_password)
        text = msg.as_string()
        server.sendmail(sent_from,to,text)
        server.close()

        print("Log file successfully send to mail")
    except Exception as E:
        print("Unable to send mail.",E)

def ProcessdisplayLog(log_dir,mail_dest):
    listProcess = []

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    seprator = "-"*80
    log_path = os.path.join(log_dir,"proc.log")
    fd = open(log_path,'w')
    fd.write(seprator + "\n")
    fd.write("Process Information :\n")
    fd.write(seprator + "\n")
    fd.write("\n")

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs = ['pid','name','username'])
            listProcess.append(pinfo)
        
        except (psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            pass

    for element in listProcess:
        fd.write("%s\n"%element)

    print("Log file successfully generated at location %s"%(log_path))    

    connected = is_connected()

    if connected:
        user = 'goreswapnil77@gmail.com'
        password = '9975949025' 
        MailSender(user,password,log_path,mail_dest)
    else:
        print("There is no internet")


def main():
    print("Send log file to  mail....")

    dir_name = argv[1]
    mail_dest = argv[2]

    ProcessdisplayLog(dir_name,mail_dest)

if __name__ == "__main__":
    main()