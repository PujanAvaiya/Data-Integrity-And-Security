import cv2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import socket
import shutil
from datetime import datetime

sendit: bool = False
flag = False
REMOTE_SERVER = "www.google.com"
img_item = ""
face_cascade = cv2.CascadeClassifier(
    'haarcascade_frontalface_alt2.xml')
cap = cv2.VideoCapture(0)


def is_connected(hostname):
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        return False


def send():
    try:
        email_user = '*************'
        email_password = '**********'
        email_send = '**************'

        subject = 'Some One Login in'

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        body = 'Alert Boss Activity Detected!'
        msg.attach(MIMEText(body, 'plain'))

        filename = 'D:/Security/Image.png'
        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= " + filename)

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)

        server.sendmail(email_user, email_send, text)
        server.quit()
        attachment.close()
        print("mail sent sucessful")
    except:
        send()


def check():
    if flag:
        while True:
                send()
                break


def last():
    try:
        now = datetime.now()
        dt_string = now.strftime("D%d%m%YT%H%M%S")
        dt_string = dt_string + ".png"
        part = "D:/Security"
        final = part + dt_string
        shutil.move("D:/Security", final)
    except Exception as e:
        print("exception:", e)


while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        roi_color = frame[y:y + h + 1000, x:x + w + 1000]
        img_item = "D:/Security/Image.png"
        cv2.imwrite(img_item, roi_color)
        sendit = True
        flag = True
        break
    if sendit:
        break
    if cv2.waitKey(20) | 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
check()
last()
