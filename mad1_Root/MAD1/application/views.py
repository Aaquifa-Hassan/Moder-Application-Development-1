from flask import current_app as app,render_template,redirect,request,session
from .models import db,User,Section,Book,BookLended


@app.route("/register",methods = ["GET","POST"])
def register():
    if request.method == "POST":
        try:
            existing = User.query.filter_by(email = request.form.get("email")).first()
            if existing:
                return render_template('register.html',error=True)
            user = User(
                username=request.form.get("username"),
                email=request.form.get("email"),
                password=request.form.get("password"),
                role = 'User'
                )
            db.session.add(user)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(e)
            return  render_template('register.html',error=True)
    return render_template("register.html")


@app.route("/",methods = ["GET","POST"])
def login():
    if request.method == "POST":
        valid = User.query.filter_by(email = request.form.get("email")).first()
        if valid is not None and valid.password ==  request.form.get("password") and valid.role != "admin":
            session["name"] = valid.username
            session["user_id"] = valid.user_id
            session['role'] = valid.role
            return redirect("/user-dashboard")
        
        return render_template("login.html",error=True)
    return render_template("login.html")

@app.route("/adminLogin",methods = ["GET","POST"])
def adminLogin():
    if request.method == "POST":
        valid = User.query.filter_by(email = request.form.get("email")).first()
        if valid is not None and valid.password == request.form.get("password") and valid.role == "admin":
            session["name"] = valid.username
            session['role'] = valid.role
            return redirect("/dashboard")
        
        return render_template("adminLogin.html",error=True)
    return render_template("adminLogin.html")


@app.route('/logout')
def logout():
    session["name"] = None
    session.clear()
    return redirect("/")


@app.route('/search',methods=['POST'])
def search():
    searchTerm = request.form['search']
    if request.form['where_search'] == 'myBooks':
        lended = BookLended.query.filter_by(user_id = session["user_id"]).all()
        if request.form['searchType'] == 'Section':
            filtered = []
            for item in lended:
                if searchTerm in item.book.section.name:
                    filtered.append(item)
            return render_template("myBooks.html",lended = filtered)

        if request.form['searchType'] == 'Title':
            filtered = []
            for item in lended:
                if searchTerm in item.book.name:
                    filtered.append(item)
            return render_template("myBooks.html",lended = filtered)
    
    if request.form['searchType'] == 'Section':
        sections = Section.query.filter(
            Section.name.like(f'%{searchTerm}%')
        ).all()
        if session['role'] == 'admin':
            return render_template('dashboard.html',sections=sections)
        else:
            return render_template('dashboard-user.html',sections=sections)
        
    if request.form['searchType'] == 'Title':
        sections = Section.query.join(Book).filter(Book.name.ilike(f'%{searchTerm}%')).distinct(Section.section_id).all()
        print(sections)

    if session['role'] == 'admin':
        return render_template('dashboard.html',sections=sections)
    else:
        return render_template('dashboard-user.html',sections=sections)
