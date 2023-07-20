
import random
import string

from flask import Flask , render_template , request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = '12345678'

url_dict = {}
with app.app_context():
    db = SQLAlchemy(app)

class table(db.Model):
    Username = db.Column(db.String(400) , primary_key = True)
    Password = db.Column(db.String(400) , nullable = False)
    shortened_url = db.Column(db.String(400) , nullable = False)
    original_url = db.Column(db.String(400) , primary_key = True)

    def __repr__(self) -> str:
        return f"{self.Username} - {self.Password} - {self.shortened_url} - {self.original_url}"

with app.app_context():
    db.create_all()

def convert_to_dict(url_dict):
    return {i.shortened_url : i.original_url for i in url_dict}

def convert_to_dict2(url_dict):
    return {i.Username : i.Password for i in url_dict}

def convert_to_dict3(url_dict):
    temp={}
    for i in url_dict:
        dell = table.query.filter_by(original_url="None").all()
        for i in dell:
            user=i.Username
            pword=i.Password
        if i.Username == user and i.Password == pword:
            temp[i.shortened_url]=i.original_url
    return temp

def shortenurl():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(8))

@app.route('/generate' , methods=['GET' , 'POST'])
def generate_url():
    if request.method=='POST':
        user= "admin"
        pword= "admin"
        originalurl = request.form['originalurl']
        shortenedurl = shortenurl()
        base = table.query.all()
        dell = table.query.filter_by(original_url="None").all()
        for i in dell:
            user=i.Username
            pword=i.Password
        url_dict=convert_to_dict(base)
        usershort = convert_to_dict3(base)
        if originalurl in url_dict.values():
            shortenedurl = list(url_dict.keys())[list(url_dict.values()).index(originalurl)]
            if shortenedurl not in usershort.keys():
                newrow = table(shortened_url = shortenedurl , original_url = originalurl , Username = user, Password = pword)
                db.session.add(newrow)
                db.session.commit()
            flash(request.url_root+shortenedurl)
            return render_template('index.html', shortenedurl=shortenedurl, originalurl=originalurl)
        while shortenedurl in url_dict:
            shortenedurl = shortenurl()
        url_dict[shortenedurl] = originalurl
        newrow = table(shortened_url = shortenedurl , original_url = originalurl , Username = user, Password = pword)
        db.session.add(newrow)
        db.session.commit()
        flash(request.url_root+shortenedurl)
        return render_template('index.html', shortenedurl=shortenedurl, originalurl=originalurl)

    return render_template('index.html')

@app.route('/gen', methods=['GET' , 'POST'])
def logged_in():
    if request.method=='POST':
        pword = request.form['PASSWORD']
        user = request.form['USERNAME']
        url_dict = table.query.all()
        url_dict=convert_to_dict2(url_dict)
        if user in url_dict.keys():
            if pword == url_dict[user]:
                newrow = table(Username = user , Password = pword ,original_url = "None" , shortened_url = "None")
                db.session.add(newrow)
                db.session.commit()
                flash("successfully logged in")
                return render_template('index.html')
            else:
                flash("Wrong Password")
                return render_template('login.html')
        else:
            newrow = table(Username = user , Password = pword , original_url = "None" , shortened_url = "None")
            db.session.add(newrow)
            db.session.commit()
            flash("successfully logged in")
            return render_template('index.html')
    return render_template('login.html')
        
    
@app.route('/',methods=['GET' , 'POST'])
def loginnn():
    dell = table.query.filter_by(original_url="None").all()
    for i in dell:
        db.session.delete(i)
        db.session.commit()
    return render_template('login.html')


@app.route('/<short_url>')
def redirect_url(short_url):
    url_dict=table.query.all()
    url_dict=convert_to_dict(url_dict)
    url=url_dict.get(short_url)
    if url:
        return redirect(url)
    else:
        return f"URL doesn't exist"

@app.route('/allurls', methods=['GET' , 'POST'])
def allurls():
    if request.method=='POST':
        dell = table.query.filter_by(original_url="None").all()
        for i in dell:
            user=i.Username
        url_dict=table.query.filter_by(Username=user).all()
        return render_template('index2.html' , alllinks = url_dict, root=request.url_root)

if __name__ == "__main__":
    app.run(debug=True,port=8000)