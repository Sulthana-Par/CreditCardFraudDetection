from flask import Flask, render_template, flash, request, session

import mysql.connector
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, jsonify
import datetime
import re

import sys
import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/NewUser")
def NewUser():
    import LiveRecognition  as liv

    del sys.modules["LiveRecognition"]

    return render_template('NewUser.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/viewproduct", methods=['GET', 'POST'])
def viewproduct():
    # searc = request.args.get('subcat')
    searc = request.form['subcat']

    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')

    cur1 = conn1.cursor()
    cur1.execute(
        "SELECT * from protb where SubCategory like '%" + searc + "%' ")
    data = cur1.fetchall()
    data1 = ''
    return render_template('ViewProduct.html', data=data, data1=data1)


@app.route("/AdminHome")
def AdminHome():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')

    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM regtb ")
    data = cur1.fetchall()
    # return 'file register successfully'
    # return render_template('order.html', data=data)

    return render_template('AdminHome.html', data=data)


@app.route("/NewProduct")
def NewProduct():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')

    cur1 = conn1.cursor()
    cur1.execute("SELECT DISTINCT ProductType FROM protb ")
    data = cur1.fetchall()

    return render_template('NewProduct.html', data=data)


@app.route("/Search")
def Search():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')

    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM protb ")
    data = cur1.fetchall()

    return render_template('ViewProduct.html', data=data)


@app.route("/ProductInfo")
def ProductInfo():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')

    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM protb ")
    data = cur1.fetchall()

    return render_template('ProductInfo.html', data=data)


@app.route("/SalesInfo")
def SalesInfo():
    return render_template('SalesInfo.html')


@app.route("/FeedBackInfo")
def FeedBackInfo():
    return render_template('FeedBackInfo.html')


@app.route("/RNewUser", methods=['GET', 'POST'])
def RNewUser():
    if request.method == 'POST':
        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        address = request.form['address']
        pnumber = request.form['phone']
        uname = request.form['uname']
        password = request.form['psw']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'

    return render_template('userlogin.html')


@app.route("/RNewProduct", methods=['GET', 'POST'])
def RNewProduct():
    if request.method == 'POST':
        file = request.files['fileupload']
        file.save("static/upload/" + file.filename)

        ProductId = request.form['pid']
        Gender = request.form['gender']
        Category = request.form['cat']
        SubCategory = request.form['subcat']
        ProductType = request.form['ptype']
        Colour = request.form['color']
        Usage = request.form['usage']
        ProductTitle = request.form['ptitle']

        Image = file.filename
        ImageURL = "static/upload/" + file.filename

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO protb VALUES ('" + ProductId + "','" + Gender + "','" + Category + "','" + SubCategory + "','" + ProductType + "','" + Colour + "','" +
            Usage + "','" + ProductTitle + "','" + Image + "','" + ImageURL + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'

    return render_template('NewProduct.html')


@app.route("/NewCard")
def NewCard():

    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM cardtb where UserName='"+ session['uname'] +"'  ")
    data = cur1.fetchall()

    return render_template('NewCardInfo.html',data=data)


@app.route("/RNewcard", methods=['GET', 'POST'])
def RNewcard():
    if request.method == 'POST':
        cno = request.form['cno']
        ctype = request.form['ctype']
        exm = request.form['exm']
        exy = request.form['exy']
        cnvo = request.form['cnvo']
        pin = request.form['pin']
        uname = session['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cardtb VALUES ('','" + uname + "','" + cno + "','" + ctype + "','" + exm + "','" + exy + "','" + cnvo + "','" +
            pin + "','Active')")
        conn.commit()
        conn.close()
        # return 'file register successfully'
    return render_template('NewCardInfo.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']
        session['count'] = 0
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where UserName='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()

        if data is None:

            data1 = 'Username or Password is wrong'
            return render_template('goback.html', data=data1)



        else:
            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')

            cur1 = conn1.cursor()
            cur1.execute("SELECT * FROM regtb where username='" + session['uname'] + "' ")
            data = cur1.fetchall()
            # return 'file register successfully'
            # return render_template('order.html', data=data)

            return render_template('UserHome.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cursor = conn.cursor()
        cursor.execute("SELECT * from admintb where UserName='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()

        if data is None:
            data1 = 'Username or Password is wrong'
            return render_template('goback.html', data=data1)

        else:

            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')

            cur1 = conn1.cursor()
            cur1.execute("SELECT * FROM regtb  ")
            data = cur1.fetchall()
            # return 'file register successfully'
            # return render_template('order.html', data=data)

            return render_template('AdminHome.html', data=data)


@app.route("/Remove", methods=['GET'])
def Remove():
    pid = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    cursor = conn.cursor()
    cursor.execute("Delete from protb  where id='" + pid + "'")
    conn.commit()
    conn.close()
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    # cursor = conn.cursor()
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM protb ")
    data = cur1.fetchall()
    # return 'file register successfully'
    return render_template('ProductInfo.html', data=data)


@app.route("/fullInfo")
def fullInfo():
    pid = request.args.get('pid')
    session['pid'] = pid

    rat1 = ''
    rat2 = ''
    rat3 = ''
    rat4 = ''
    rat5 = ''

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  ROUND(AVG(Rate), 1) as numRating FROM reviewtb WHERE ProductId  ='" + pid + "' ")
    data2 = cursor.fetchone()
    print(data2[0])
    if data2 is None:
        avgrat = 0
    else:
        if data2[0] == 'None':
            avgrat = 0
            if (int(avgrat) == 1):
                rat1 = 'checked'
            if (int(avgrat) == 2):
                rat2 = 'checked'
            if (int(avgrat) == 3):
                rat3 = 'checked'
            if (int(avgrat) == 4):
                rat4 = 'checked'
            if (int(avgrat) == 5):
                rat5 = 'checked'
        else:
            avgrat = data2[0]

            if (avgrat == 1):
                rat1 = 'checked'
            if (avgrat == 2):
                rat2 = 'checked'
            if (avgrat == 3):
                rat3 = 'checked'
            if (avgrat == 4):
                rat4 = 'checked'
            if (avgrat == 5):
                rat5 = 'checked'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  count(Rate)  as numRating FROM reviewtb WHERE ProductId  ='" + pid + "' ")
    data3 = cursor.fetchone()
    if data3:
        avgrat = data3[0]

    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    cur = conn.cursor()
    cur.execute("SELECT UserName,Review FROM reviewtb where ProductId='" + pid + "' ")
    reviewdata = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb where ProductId='" + pid + "' ")
    data1 = cur.fetchall()

    number = pid

    pricelist = str(int(str(number)[:3]))

    return render_template('ProductFullInfo.html', data=data1, pricelist=pricelist, avgrat=avgrat, rat1=rat1, rat2=rat2,
                           rat3=rat3, rat4=rat4, rat5=rat5, reviewdata=reviewdata)


@app.route("/Book", methods=['GET', 'POST'])
def Book():
    if request.method == 'POST':

        uname = session['uname']
        pid = session['pid']

        qty = request.form['qty']

        Bookingid = ''
        ProductName = ''
        UserName = uname
        Mobile = ''
        Email = ''
        Qty = qty
        Amount = ''

        CardType = ''
        CardNo = ' '
        CvNo = ''
        date = datetime.datetime.now().strftime('%d-%b-%Y')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM protb where  ProductId='" + pid + "'")
        data = cursor.fetchone()

        if data:
            ProductName = data[7]
            price = str(int(str(data[0])[:3]))

            Amount = float(price) * float(Qty)

            print(Amount)
            session['amt'] = Amount


        else:
            return 'Incorrect username / password !'

        string = ProductName
        new_string = re.sub(r"[^a-zA-Z0-9]", "", string)
        print(new_string)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM  regtb where  UserName='" + uname + "'")
        data = cursor.fetchone()

        if data:
            Mobile = data[4]
            Email = data[3]


        else:
            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cursor = conn.cursor()
        cursor.execute("SELECT  count(*) as count  FROM  booktb  ")
        data = cursor.fetchone()

        if data:
            count = data[0]

            if count == 0:
                count = 1;
            else:
                count += 1




        else:
            return 'Incorrect username / password !'
        print(count)

        Bookingid = "BOOKID00" + str(count)
        session['bid'] = Bookingid

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO booktb VALUES ('','" + Bookingid + "','" + pid + "','" + new_string + "','" + uname + "','" + Mobile + "','" + Email + "','" + str(
                Qty) + "','" + str(Amount) + "','" + str(CardType) + "','" + str(CardNo) + "','" + str(
                CvNo) + "','" + str(date) + "','0')")
        conn.commit()
        conn.close()
        # return 'file register successfully'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cur = conn.cursor()
        cur.execute("SELECT CardNo FROM cardtb where  UserName= '" + uname + "' ")
        data = cur.fetchall()

    return render_template('Payment.html', Amount=Amount,data=data)


@app.route("/pay", methods=['GET', 'POST'])
def pay():
    if request.method == 'POST':
        cno = request.form['cno']
        pinno = request.form['pinno']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM cardtb where  UserName='" + session['uname'] + "' and CardNo ='"+ cno +"' and pin='"+ pinno +"' and Status='Active' ")
        data = cursor.fetchone()

        if data:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
            cursor = conn.cursor()
            cursor.execute("truncate table temptb")
            conn.commit()
            conn.close()

            import LiveRecognition1  as liv1
            del sys.modules["LiveRecognition1"]

            uname = session['uname']

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
            cursor = conn.cursor()
            cursor.execute("SELECT * from temptb where UserName='" + uname + "' ")
            data = cursor.fetchone()
            if data is None:

                sendmsg("","Unknown User Access Your Account IP"+IPAddr)
                flash('Face  is wrong')
                return render_template('Payment.html')
            else:
                # uname = session['uname']
                bid = session['bid']



                conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
                cursor = conn.cursor()
                cursor.execute(
                    "update booktb set Status='1'  where Bookid='" + bid + "'")
                conn.commit()
                conn.close()

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
                cur = conn.cursor()
                cur.execute("SELECT * FROM booktb where  UserName= '" + uname + "' and Status='1' ")
                data = cur.fetchall()

                flash('Payment Successful')


                return render_template('Payment.html')


        else:
            session['count'] += 1

            if session['count']==3:

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
                cursor = conn.cursor()
                cursor.execute(
                    "update cardtb set Status='Blocked'  where  UserName='" + session['uname'] + "' and CardNo ='"+ cno +"' and pin='"+ pinno +"'")
                conn.commit()
                conn.close()
                flash('Card Blocked')
                return render_template('Payment.html')
            flash('Pin Incorrect!')
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
            cur = conn.cursor()
            cur.execute("SELECT CardNo FROM cardtb where  UserName= '" +session['uname'] + "' ")
            data = cur.fetchall()
            return render_template('Payment.html',Amount=session['amt'],data=data)







def examvales1():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM regtb where  UserName='" + uname + "'")
    data = cursor.fetchone()

    if data:
        Email = data[3]
        Phone = data[4]


    else:
        return 'Incorrect username / password !'

    return uname, Email, Phone


@app.route("/UOrderInfo")
def UOrderInfo():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM booktb where  UserName= '" + uname + "' and Status='1' ")
    data = cur.fetchall()

    return render_template('UOrderInfo.html', data=data)


@app.route("/UserHome")
def UserHome():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where  UserName= '" + uname + "' ")
    data = cur.fetchall()

    return render_template('UserHome.html', data=data)


@app.route("/Review")
def Review():
    pid = request.args.get('pid')
    session['rpid'] = pid

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  protb where  ProductId='" + pid + "'")
    data = cursor.fetchone()

    if data:
        pname = data[7]



    else:
        return 'Incorrect username / password !'

    return render_template('NewReview.html', pname=pname)


@app.route("/ureview", methods=['GET', 'POST'])
def ureview():
    if request.method == 'POST':

        uname = session['uname']
        pid = session['rpid']

        pname = request.form['pname']

        feedback = request.form['feed']

        star = request.form['star']

        ProductId = ''
        ProductType = ''
        ProductName = ''
        Price = ''
        Image = ''
        UserName = uname
        Rate = star
        Review = feedback
        Result = ''

        if (int(star) > 2):
            Result = 'postive'
        else:
            Result = 'nagative'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM  protb where  ProductId='" + pid + "'")
        data = cursor.fetchone()
        if data:

            ProductId = data[0]
            ProductType = data[4]
            ProductName = data[7]
            Price = str(int(str(data[0])[:3]))
            Image = data[9]


        else:
            return 'Product Info Not Avalible..!'

        string = ProductName
        new_string = re.sub(r"[^a-zA-Z0-9]", "", string)
        print(new_string)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  reviewtb VALUES ('','" + str(ProductId) + "','" + ProductType + "','" + str(
                new_string) + "','" + str(
                Price) + "','" + str(Image) + "','" + str(UserName) + "','" + str(Rate) + "','" + str(
                Review) + "','" + str(Result) + "')")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
        cur = conn.cursor()
        cur.execute("SELECT * FROM reviewtb where  UserName= '" + uname + "' ")
        data = cur.fetchall()

        return render_template('UReviewInfo.html', data=data)


@app.route("/UReviewInfo")
def UReviewInfo():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviewtb where  UserName= '" + uname + "' ")
    data = cur.fetchall()

    return render_template('UReviewInfo.html', data=data)


@app.route("/AReviewInfo")
def AReviewInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviewtb  ")
    data = cur.fetchall()

    return render_template('AReviewInfo.html', data=data)


@app.route("/ASalesInfo")
def ASalesInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2creditcardpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM booktb  ")
    data = cur.fetchall()

    return render_template('ASalesInfo.html', data=data)


def sendmsg(targetno,message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")




if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
