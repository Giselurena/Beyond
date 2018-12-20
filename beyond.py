"""
    Beyond
    Developers:

    To run this you need to execute the following shell commands
    % pip3 install flask
    % pip3 install flask_oauthlib
    % pip3 install pickledb
    % python3 beyond.py

    For windows just don't type the "3"s

    The authentication comes from an app by Bruno Rocha
    GitHub: https://github.com/rochacbruno
"""
from functools import wraps
from flask import Flask, redirect, url_for, session, request, jsonify, render_template, request
from flask_oauthlib.client import OAuth
from datetime import datetime


reviews=[]



app = Flask(__name__)
#gracehopper.cs-i.brandeis.edu:5100
#app.config['GOOGLE_ID'] = '783502545148-diqpd39e4ldf3cug5mnh5eee7st9lhf9.apps.googleusercontent.com'
#app.config['GOOGLE_SECRET'] = 'rsz-adgWg936wtiNW6Tj-z7g'

#127.0.0.1:5000
app.config['GOOGLE_ID'] = '246096591118-ti33uv184e4m1bib9grgn8alm45btadb.apps.googleusercontent.com'
app.config['GOOGLE_SECRET'] = 'iqgLqu6pXgLuHsZFq6nvxDX3'


app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not('google_token' in session):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/main')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        print("logged in")
        print(jsonify(me.data))
        return render_template("main.html")
        #return jsonify({"data": me.data})
    print('redirecting')
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    #
    return redirect(url_for('main'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    print(session['google_token'])
    me = google.get('userinfo')
    session['userinfo'] = me.data
    print(me.data)
    return render_template("main.html")
    #return jsonify({"data": me.data})


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')





@app.route('/')
def main():
    print("rendering main.html")
    return render_template("main.html")

@app.route('/team')
def bio():
    return render_template('team.html')


results = []
@app.route('/survey', methods=['GET','POST'])
#@require_login
def survey():
    global results

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        weight = request.form['weight']
        height = request.form['height']
        location = request.form['location']
        feedback = request.form['feedback']
        time = datetime.now()

        if location == "Arm Exercises":
            feedback = """
            Doing Pushups is a great way to tone your arms!
            It is perfect for building muscles in the arms, chest, triceps and the front of the shoulders.

            Instructions:
            Position your body with your arms straight out, shoulder width apart, abs tight, holding your body in a plank position.
            Lower your body until your chest is an inch or two above the floor, elbows pulling back at roughly a 45-degree angle.
            Push your torso away from the ground until your arms lock, then repeat.

            Do 10 of these and Rest for 10 seconds. Do 3 reps of this.
            """
        elif location == "Leg Exercises":
            feedback = """
            Hello, """ + name + """, welcome to the lower body part exercises!
            Section: Gluteus

            Squats-

            Make sure to be standing straight with feet hip-width apart. Your feet needs to be apart, directly under your hips, and for balance and posture place your hands on your hips.
            It is important to flex and tighten your stomach muscles, to produce core muscle balance and strengthen your gluteus.
            Now, slowly lower down, as if sitting on a chair. Maintain good posture and keep heels on the ground. Make sure to not let your knees move inward or too outward.
            When reaching the sitting position, slowly straighten your legs.
            Repeat the movement up to 15 repetitions.

            Lunges-

            For lunges it is essential to keep your upper body straight, with your shoulders back and relaxed and chin up. A great tip is to pick a point to stare at in front of you so you don't keep looking down. Always engage your core, flex and tighten your stomach muscles, to produce core muscle balance and strengthen your spinal cord.
            Step forward with one leg, lowering your hips until both knees are bent at about a 90-degree angle.
            Keep balance at all times, the slower you go, the more concentration and perfect posture you will produce for the best results.
            Repeat up to 15 repetitions back and 15 forward.
            """
        else:
            feedback = """
            Planks help you to build strength in your core, upper and lower body so its a good full body work out.

            Start by getting into a press-up position.
            Bend your elbows and rest your weight on your forearms and not on your hands.
            Your body should form a straight line from shoulders to ankles.
            Engage your core by sucking your belly button into your spine.
            Hold this position 30 seconds and Rest for 10 seconds. Do 3 reps

            We’re going to continue on with
            The Inchworm.
            This helps work out the shoulders, abs, and back.

            Start standing with feet hip-width apart. Hinge forward at your hips and place your palms on the mat. You can bend your knees if needed to get your palms flat on the floor.
            Walk your hands forward so that you’re in high plank. Your shoulders should be stacked directly above your wrists.
            For an extra challenge, add a push-up.
            Walk your hands back toward feet and stand up.

            """

        result = {
            'name':name,
            'age':age,
            'weight':weight,
            'height':height,
            'location':location,
            'feedback':feedback,
            'time':time.strftime("%H:%M %m/%d/%y")
        }

        # messages
        results.insert(0, result) # add form object to the front of the list
        print(results)


        return render_template("report.html",  result=result)
    else:
        return render_template("survey.html")



@app.route('/show')
#@require_login
def show():
    return render_template('show.html',results=results)

@app.route('/gisel')
def person1():
    return render_template('gisel.html')


@app.route('/nana')
def person2():
    return render_template('nana.html')

@app.route('/darlene')
def person3():
    return render_template('darlene.html')

@app.route('/kamil')
def person4():
    return render_template('kamil.html')

if __name__ == '__main__':
    app.run('127.0.0.1',port=5000)  # development
    #app.run('0.0.0.0',port=5100)  # production
