from flask import current_app as app,render_template,redirect,request,session
from .models import db,User,Section,Book,BookLended,BookRequest
from datetime import datetime,timedelta, date


@app.route('/dashboard')
def dashboard():
    sections = Section.query.all()
    return render_template('dashboard.html',sections=sections)

@app.route('/add-book', methods=['GET', 'POST'])
def addBook():
    sections = Section.query.all()
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        price = request.form['price']
        author = request.form['author']
        date_issued = datetime.strptime(request.form['date_issued'], '%Y-%m-%d').date()
        return_date = request.form['return_date']
        ExistingSection = request.form['ExistingSection']
        NewSection = request.form['NewSection']
        sectionId = None

        checkName = Book.query.filter_by(name = name).first()
        if checkName:
            return render_template('addBook.html',sections=sections,error = 'A book already exits in this name')
        
        if ExistingSection == 'Default' and not NewSection:
            return render_template('addBook.html',sections=sections,error = 'Fill any one of the Optional fields')
    
        if ExistingSection != 'Default':
            sectionId = int(request.form['ExistingSection'])

        if ExistingSection =='Default':
            existing = Section.query.filter_by(name = NewSection).first()
            if existing:
                return render_template('addBook.html',sections=sections,error = 'A Section already exists in this name')
            if not existing:
                new_section = Section(name = NewSection)
                db.session.add(new_section)
                db.session.commit()
                sectionId = new_section.section_id

        new_book = Book(
                        name=name,
                        content=content,
                        author=author,
                        date_issued=date_issued,
                        return_date=return_date,
                        section_id=sectionId,
                        price=price
                        )

        db.session.add(new_book)
        db.session.commit()
        return redirect('/dashboard') 
     
    current_date = date.today().isoformat()
    print("type")
    return render_template('addBook.html', sections=sections, current_date=current_date)


@app.route('/update-book', methods=['GET', 'POST'])
def updateBook():
    sections = Section.query.all()
    if request.form['method'] == 'PUT':
        name = request.form['name']
        content = request.form['content']
        price = request.form['price']
        author = request.form['author']
        date_issued = request.form['date_issued']
        return_date = request.form['return_date']
        ExistingSection = request.form['ExistingSection']
        NewSection = request.form['NewSection']

        toUpdate = Book.query.filter_by(book_id = session['update_book_id']).first()
        if not toUpdate:
            return render_template('updateBook.html',sections=sections,error='Book not found')
        
        if name:
            checkName = Book.query.filter_by(name = name).first()
            if checkName:
                return render_template('addBook.html',sections=sections,error = 'A book already exits in this name')
            toUpdate.name = name
        if price:
            toUpdate.price = price
        if content:
            toUpdate.content = content
        if author:
            toUpdate.author = author
        if date_issued:
            toUpdate.date_issued = datetime.strptime(date_issued, '%Y-%m-%d').date()
        if return_date:
            toUpdate.return_date = return_date
        if ExistingSection != 'Default':
            toUpdate.section_id = int(request.form['ExistingSection'])
        
        if ExistingSection =='Default' and NewSection:
            existing = Section.query.filter_by(name = NewSection).first()
            if existing:
                return render_template('updateBook.html',sections=sections,error = 'A Section already exists in this name')
            if not existing:
                new_section = Section(name = NewSection)
                db.session.add(new_section)
                db.session.commit()
                toUpdate.section_id = new_section.section_id
        
        db.session.commit()
        return redirect('/dashboard')
    
    session['update_book_title'] = request.form['book_title']
    session['update_book_id'] = request.form['book_id']
    session['update_book_section'] = request.form['section']
    current_date = date.today().isoformat()
    return render_template('updateBook.html',sections=sections, current_date=current_date)




@app.route('/delete-book',methods=['POST'])
def deleteBook():
    if request.form['method'] == 'DELETE':
        toDelete = Book.query.filter_by(book_id = session['delete_book_id']).first()
        if not toDelete:
            return render_template('deleteBook.html',error="Book doesn't exists")
        db.session.delete(toDelete)
        db.session.commit()
        return redirect('/dashboard')
    session['delete_book_title'] = request.form['book_name']
    session['delete_book_id'] = request.form['book_id']
    session['delete_book_section'] = request.form['section']
    return render_template('deleteBook.html')



@app.route('/update-section',methods=['POST'])
def updateSection():
    if request.form['method'] == 'PUT':
        new_name = request.form['new_name']
        existing = Section.query.filter_by(name= new_name).first()
        if existing:
            return render_template('updateSection.html',error='Section already exists!')
        toUpdate = Section.query.filter_by(name = session["update_section"]).first()
        toUpdate.name = new_name
        db.session.commit()

        return redirect('/dashboard')

    session["update_section"] = request.form['update_section']
    return render_template('updateSection.html')



@app.route('/delete-section',methods=['POST'])
def deleteSection():
    if request.form['method'] == 'DELETE':
        toDelete = Section.query.filter_by(name= session["delete_section"]).first()
        if not toDelete:
            return render_template('deleteSection.html',error="Section Doesn't exists!")
        for book in toDelete.books:
            db.session.delete(book)
        db.session.delete(toDelete)
        db.session.commit()

        return redirect('/dashboard')
    
    session["delete_section"] = request.form['delete_section']
    return render_template('deleteSection.html')


@app.route('/user-access',methods=['GET','POST'])
def userAccess():
    requests = BookRequest.query.all()
    supplied = BookLended.query.all()
    return render_template('userAccess.html',requests=requests,supplied=supplied)

@app.route('/approve-request',methods=['GET','POST'])
def approveRequest():
    if request.method == 'POST':
        book_id = request.form['book_id']
        user_id = request.form['user_id']
        return_date = request.form['return_date']

        lend = BookLended(
                        book_id = book_id,
                        user_id = user_id,
                        return_date = datetime.now() + timedelta(days=int(return_date))
                        )
        if lend:
            db.session.add(lend)
            db.session.commit()

        delete = BookRequest.query.filter_by(book_id = book_id,user_id = user_id).first()
        if delete:
            db.session.delete(delete)
            db.session.commit()
        return redirect("/user-access")

@app.route('/delete-request',methods=['GET','POST'])
def deleteRequest():
    if request.method == 'POST':
        book_id = request.form['book_id']
        user_id = request.form['user_id']
        delete = BookRequest.query.filter_by(book_id = book_id,user_id = user_id).first()
        if delete:
            db.session.delete(delete)
            db.session.commit()
        return redirect("/user-access")
    

@app.route('/revoke',methods=['GET','POST'])
def revoke():
    if request.method == 'POST':
        book_id = request.form['book_id']
        user_id = request.form['user_id']
        delete = BookLended.query.filter_by(book_id = book_id,user_id = user_id).first()
        if delete:
            db.session.delete(delete)
            db.session.commit()
        return redirect("/user-access")