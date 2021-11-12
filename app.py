from flask import Flask, render_template, request, url_for
from fetch import fetch_from_db
from user_management import User
from insert_paper import insert_paper

app = Flask(__name__)
app.secret_key = "hi there"
user = User()

conferences = [{"publisher": "IEEE"}, {"publisher": "IOS Press"}, {
    "publisher": "IEEE Computer Society"}, {"publisher": "Springer"}]

topics = [{"subject": "Machine Learning"}, {
    "subject": "Cyber Security"}, {"subject": "Internet of things"}]


@app.route('/')
def index():
    return render_template('index.html', theme=1)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/ans', methods=['POST', 'GET'])
def login_ans():
    user.logout()
    name = request.form['username']
    pwd = request.form['password']
    a = user.login(name, pwd)
    if a == 1:
        return render_template('org_insertion.html', theme=1)
    elif a == -1:
        return render_template('org_insertion.html', theme=1)
    elif a == -2:
        return render_template('login.html', info="invalid username")
    elif a == -3:
        return render_template('login.html', info="invalid password")
    elif a == -4:
        return render_template('login.html', info="another user is  logged in")


# @app.route('/register')
# def show_regeistration_page():
#     return render_template('register.html')


@app.route('/register_in', methods=['POST', 'GET'])
def register_user():
    a = user.register(request.form['username'], request.form['password'],
                      request.form['email'], request.form['department'])
    if a == 1:
        return render_template('login.html')
    elif a == -1:
        return "username taken"
    elif a == -2:
        return "email taken"


@app.route('/register')
def register():
    return render_template('registration.html')


@app.route('/register/ans', methods=['POST', 'GET'])
def register_ans():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    department = request.form['department']
    check = user.register(username, password, email, department)
    if check == -1:
        return render_template('registration.html', info='Username already exixsts!')
    elif check == -2:
        return render_template('registration.html', info=' Email already exists!')
    else:
        return render_template('registration.html', info="Registered successfully !!!!")


@app.route('/search', methods=['POST', 'GET'])
def search():
    query = request.form['search_query']
    # return render_template('ans.html', info=query)
    posts = fetch_from_db(query)
    return render_template('home.html', posts=posts, title="Paper Ranker", theme=1, conferencesList=conferences, topicList=topics)


@app.route('/org_insertion', methods=['POST', 'GET'])
def org_insertion():
    if(user.check()):
        details = dict()
        details['title'] = request.form['title']
        details['authors'] = request.form['authors'].split(',')
        details['venue'] = request.form['venue']
        details['year'] = request.form['year']
        details['access'] = request.form['access']
        details['url'] = request.form['url']
        details['rank'] = request.form['rank']
        details['keywords'] = request.form['field'].split(',')
        # print(details)
        insert_paper(details)
        return render_template('org_insertion.html', theme=1)

    else:
        return render_template('login.html', info='You are not logged in')


@app.route('/logout')
def log_out():
    user.logout()
    return render_template('login.html', theme=1)


if __name__ == "__main__":
    app.run(debug=True)
