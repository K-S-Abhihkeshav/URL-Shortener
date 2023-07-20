#basic algo to shorten a URL link

import json
import random
import string

from flask import Flask, redirect, request, render_template, url_for

app=Flask(__name__)

with app.app_context():
    db=SQLAlchemy(app)

class table(db.Model):
    original_url=db.Column(db.String(400), primary_key=True)
    short_url=db.Column(db.String(400), unique=True, nullable=False)

    def __repr__(self):
        return f"table('{self.original_url}','{self.short_url}')"

with app.app_context():
    db.create_all()

url_dict = {}

def generate_short_url():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(8))

@app.route("/", methods=['GET', 'POST'])
def create_url():
        if request.method == 'POST':
            url = request.method['originalurl']
            short_url = generate_short_url()
            while short_url in url_dict:
                short_url = generate_short_url()
            newrow=table(original_url=url,short_url=short_url)
            db.session.add(newrow)
            db.session.commit()
            return "new short url: {request.url_root}{short_url}"
        return render_template('index.html')

@app.route('/<short_url>')

def redirect_url(short_url):
    url=url_dict.get(short_url)
    return redirect(url)

if __name__ == "__main__":
    app.run(debug=True,port=8000)

