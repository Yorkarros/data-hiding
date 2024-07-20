from flask import Flask, render_template, request, session, flash
from ecies.utils import generate_key
from ecies import encrypt, decrypt
import mysql.connector
import base64, os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from base64 import b64encode, b64decode
import secrets
import string
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/SenderLogin')
def SenderLogin():
    return render_template('SenderLogin.html')


@app.route('/ReceiverLogin')
def ReceiverLogin():
    return render_template('ReceiverLogin.html')


@app.route('/NewReceiver')
def NewReceiver():
    return render_template('NewReceiver.html')


@app.route('/NewSender')
def NewSender():
    return render_template('NewSender.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM sendertb ")
            data = cur.fetchall()
            flash("you are successfully Login")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM sendertb  ")
    data = cur.fetchall()
    return render_template('ReceiverInfo.html', data=data)


@app.route("/ReceiverInfo")
def ReceiverInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM recivertb  ")
    data = cur.fetchall()
    return render_template('ReceiverInfo.html', data=data)


@app.route("/MessageInfo")
def MessageInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM msgtb  ")
    data = cur.fetchall()
    return render_template('MessageInfo.html', data=data)


@app.route("/newsender", methods=['GET', 'POST'])
def newsender():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into sendertb values('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "')")
        conn.commit()
        conn.close()
        flash("Record Saved!")

    return render_template('SenderLogin.html')


@app.route("/senderlogin", methods=['GET', 'POST'])
def senderlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['sname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from sendertb where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            flash('Username or Password is wrong')
            return render_template('SenderLogin.html', data=data)

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM sendertb where username='" + username + "' and password='" + password + "'")
            data = cur.fetchall()
            flash("you are successfully logged in")
            return render_template('SenderHome.html', data=data)


@app.route('/SenderHome')
def SenderHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
    cur = conn.cursor()
    cur.execute("SELECT username FROM sendertb  where username='" + session['sname'] + "' ")
    data = cur.fetchall()
    return render_template('SendMessage.html', data=data)


@app.route('/SendMessage')
def SendMessage():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
    cur = conn.cursor()
    cur.execute("SELECT username FROM recivertb  ")
    data = cur.fetchall()
    return render_template('SendMessage.html', data=data)


@app.route('/UploadVideo')
def UploadVideo():
    return render_template('UploadVideo.html')


@app.route("/viupload", methods=['GET', 'POST'])
def viupload():
    if request.method == 'POST':
        file = request.files['file']

        file.save("static/upload/" + file.filename)

        import cv2

        # Path to video file
        vidObj = cv2.VideoCapture("static/upload/" + file.filename)

        # Used as counter variable
        count = 0

        # checks whether frames were extracted
        success = 1

        while success:
            # vidObj object calls read
            # function extract frames
            success, image = vidObj.read()

            # Saves the frames with frame-count
            cv2.imwrite("./static/frame/frame%d.jpg" % count, image)

            count += 1

        flash(' Video Convert To Frame  Successfully!')
        return render_template('UploadVideo.html')


@app.route('/HideAudio')
def HideAudio():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
    cur = conn.cursor()
    cur.execute("SELECT username FROM recivertb  ")
    data = cur.fetchall()
    return render_template('HideAudio.html', data=data)


import wave


def em_audio(af, string, output):
    waveaudio = wave.open(af, mode='rb')
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    string = string + int((len(frame_bytes) - (len(string) * 8 * 8)) / 8) * '#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    frame_modified = bytes(frame_bytes)
    with wave.open(output, 'wb') as fd:
        fd.setparams(waveaudio.getparams())
        fd.writeframes(frame_modified)
    waveaudio.close()
    print("Done...")


def ex_msg(af):
    print("Please wait...")
    waveaudio = wave.open(af, mode='rb')
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    msg = string.split("###")[0]
    print("Your Secret Message is: \033[1;91m" + msg + "\033[0m")
    waveaudio.close()


@app.route("/waupload", methods=['GET', 'POST'])
def waupload():
    if request.method == 'POST':

        import random
        file1 = request.files['file1']
        fnew1 = random.randint(1111, 9999)
        savename1 = str(fnew1) + file1.filename
        file1.save("static/upload/" + savename1)



        import random
        file2 = request.files['file2']
        fnew2 = random.randint(1111, 9999)
        savename2 = str(fnew2) + file2.filename
        file2.save("static/upload/" + savename2)

        rname = request.form['rname']
        hinfo = savename1 + ","+savename2
        hkey = request.form['hkey']

        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + file.filename
        file.save("static/upload/" + savename)

        inname = "./static/upload/" + savename

        outname = "./static/Encode/" + savename

        em_audio(inname, hinfo, outname)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM recivertb where  UserName='" + rname + "'")
        data = cursor.fetchone()

        if data:
            email = data[3]


        else:
            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO msgtb VALUES ('','" + session[
                'sname'] + "','" + rname + "','" + email + "','" + savename + "','" + hkey + "','Audio')")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
        cursor = conn.cursor()
        cursor.execute("SELECT  max(id) as id   FROM recivertb ")
        data2 = cursor.fetchone()

        if data2:
            maxid = data2[0]

    flash(' Image Hide Successfully!')
    sendmail(email, " Hide id" + str(maxid) + "Unhidekey" + hkey)

    return render_template('HideAudio.html')


@app.route("/imupload", methods=['GET', 'POST'])
def imupload():
    if request.method == 'POST':
        from stegano import lsb
        from PIL import Image

        rname = request.form['rname']
        hinfo = request.form['hinfo']
        hkey = request.form['hkey']

        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)
        image = Image.open("./static/upload/" + savename)
        print(f"Original size : {image.size}")  # 5464x3640
        sunset_resized = image.resize((400, 400))
        sunset_resized.save("./static/upload/" + savename)

        secret = lsb.hide("./static/upload/" + savename, hinfo)

        pathname, extension = os.path.splitext("./static/upload/" + savename)
        filename = pathname.split('/')
        imageName = filename[-1] + ".png"
        secret.save("./static/Encode/" + imageName)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM recivertb where  UserName='" + rname + "'")
        data = cursor.fetchone()

        if data:
            email = data[3]


        else:
            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO msgtb VALUES ('','" + session[
                'sname'] + "','" + rname + "','" + email + "','" + savename + "','" + hkey + "','image')")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
        cursor = conn.cursor()
        cursor.execute("SELECT  max(id) as id   FROM recivertb ")
        data2 = cursor.fetchone()

        if data2:
            maxid = data2[0]

    flash(' Image Hide Successfully!')
    sendmail(email, " Hide id" + str(maxid) + "Unhidekey" + hkey)

    return render_template('SendMessage.html')


@app.route('/SMessageInfo')
def SMessageInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM msgtb where SenderName='" + session['sname'] + "' ")
    data = cur.fetchall()
    return render_template('SMessageInfo.html', data=data)


@app.route("/newreceiver", methods=['GET', 'POST'])
def newreceiver():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into recivertb values('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "')")
        conn.commit()
        conn.close()
        flash("Record Saved!")
    return render_template('ReceiverLogin.html')


@app.route("/receiverlogin", methods=['GET', 'POST'])
def receiverlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['rname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from recivertb where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            flash('Username or Password is wrong')
            return render_template('ReceiverLogin.html', data=data)

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM recivertb where username='" + username + "' and password='" + password + "'")
            data = cur.fetchall()
            flash("you are successfully logged in")
            return render_template('ReceiverHome.html', data=data)


@app.route('/ReceiverHome')
def ReceiverHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
    cur = conn.cursor()
    cur.execute("SELECT username FROM sendertb  where username='" + session['rname'] + "' ")
    data = cur.fetchall()
    return render_template('SendMessage.html', data=data)


@app.route('/RMessageInfo')
def RMessageInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM msgtb where ReceiverName='" + session['rname'] + "'  ")
    data = cur.fetchall()
    return render_template('RMessageInfo.html', data=data)


@app.route("/vdecrypt")
def vdecrypt():
    id = request.args.get('id')
    ty = request.args.get('ty')

    if ty == "image":
        session["rhcid"] = id
        imname1 = request.args.get('imname')
        mimage = 'static/Encode/' + imname1
        return render_template('HDView.html', iname=mimage)
    else:
        session["rhcid"] = id
        return render_template('HDView1.html')


@app.route("/hvdown", methods=['GET', 'POST'])
def hvdown():
    if request.method == 'POST':
        uhkey = request.form['hkey']

        from stegano import lsb

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM msgtb where  id='" + session["rhcid"] + "'")
        data = cursor.fetchone()

        if data:
            imid = data[4]
            hKey = data[5]

        else:
            return 'Incorrect username / password !'

        if uhkey == hKey:
            flash('Successfully Unhide Message!')
            clear_message = lsb.reveal('static/Encode/' + imid)
            mimage = 'static/Encode/' + imid

            print(clear_message)
            return render_template('HDView.html', iname=mimage, pre=clear_message)
        else:
            mimage = 'static/Encode/' + imid
            flash('Your Unhide key  Incorrect!')
            return render_template('HDView.html', iname=mimage)


@app.route("/hvdown1", methods=['GET', 'POST'])
def hvdown1():
    if request.method == 'POST':
        uhkey = request.form['hkey']

        from stegano import lsb

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3datahideivadb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM msgtb where  id='" + session["rhcid"] + "'")
        data = cursor.fetchone()

        if data:
            imid = data[4]
            hKey = data[5]

        else:
            return 'Incorrect username / password !'

        if uhkey == hKey:

            mimage = 'static/Encode/' + imid

            print("Please wait...")
            waveaudio = wave.open(mimage, mode='rb')
            frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
            extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
            string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
            msg = string.split("###")[0]
            print("Your Secret Message is: \033[1;91m" + msg + "\033[0m")
            waveaudio.close()
            flash('Successfully Unhide Message!')

            splitted_string = msg.split(',')


            return render_template('HDView2.html', img1="static/upload/"+splitted_string[0],img2="static/upload/"+splitted_string[1])
        else:

            flash('Your Unhide key  Incorrect!')
            return render_template('HDView1.html')


def sendmail(Mailid, message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = Mailid

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "qmgn xecl bkqv musr")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
