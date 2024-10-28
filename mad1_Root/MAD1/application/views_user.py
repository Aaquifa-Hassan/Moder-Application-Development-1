from flask import current_app as app,render_template,redirect,request,session,send_file
from .models import db,User,Section,Book,Feedback,BookRequest,BookLended
from weasyprint import HTML
from datetime import datetime

@app.route('/user-dashboard')
def user_dashboard():
    sections = Section.query.all()
    return render_template('dashboard-user.html',sections=sections)


@app.route('/feedback',methods=['POST'])
def feedback():
    if request.form['confirmation'] == 'CONFIRM':
        feedback = request.form['feedback']
        if not feedback:
            return render_template('feedback.html',error='Write something before submitting!')
        entry = Feedback(user_id = session["user_id"],book_id = session['book_id'],feedback_text = feedback)
        db.session.add(entry)
        db.session.commit()

        if session['to_where'] == 'from_mybooks':
            return redirect('/my-books')
        return redirect('/user-dashboard')
    
    session['book_title'] = request.form['book_title']
    session['book_id'] = request.form['book_id']
    session['section_name'] = request.form['section_name']
    session['section_id'] = request.form['section_id']
    session['to_where'] = request.form['to_where']
    return render_template('feedback.html')

@app.route('/request',methods=['POST'])
def requesting():
    if request.form['confirmation'] == 'CONFIRM':
        newRequest = BookRequest(user_id = session["user_id"],book_id = session['book_id'])
        db.session.add(newRequest)
        db.session.commit()
        return redirect('/user-dashboard')
    
    totalRequests = BookRequest.query.filter_by(user_id = session["user_id"]).all()
    if len(totalRequests) == 5:
        return render_template('userRequesting.html',limitError = "Only a maximum of 5 books can be requested")
    
    session['book_title'] = request.form['book_title']
    session['book_id'] = request.form['book_id']
    session['section_name'] = request.form['section_name']
    session['section_id'] = request.form['section_id']

    exists = BookRequest.query.filter_by(user_id = session["user_id"],book_id = session['book_id']).first()
    if exists:
        return render_template('userRequesting.html',error = f"book '{session['book_title']}' is already been requested")
    return render_template('userRequesting.html')


@app.route('/my-books',methods=["GET","POST"])
def myBooks():
    lended = BookLended.query.filter_by(user_id = session["user_id"]).all()
    lended = BookLended.query.filter_by(user_id = session["user_id"]).all()
    for item in lended:
        if item.return_date.date() <= datetime.now().date() :
            db.sesion.delete(item)
            db.session.commit()
    return render_template("myBooks.html",lended = lended)


@app.route('/return',methods=["GET","POST"])
def Return():
    if request.form['confirmation'] == 'CONFIRM':
        delete = BookLended.query.filter_by(
                                        book_id = session['return_book_id'],
                                        user_id = session["user_id"]
                                        ).first()
        if delete:
            db.session.delete(delete)
            db.session.commit()
        return redirect('/my-books')
    
    session['return_book_title'] = request.form['book_title']
    session['return_book_id'] = request.form['book_id']
    return render_template('returnBook.html')


@app.route('/purchase',methods=["GET","POST"])
def puchace():
    if request.form['confirmation'] == 'CONFIRM':
        book = Book.query.filter_by(book_id=session['purchase_book_id']).first()
        book_name = book.name
        author = book.author
        content = book.content
        html_content = f"<html><body><h1>{book_name}</h1><p>Author: {author}</p><p>{content}</p></body></html>"
        pdf_filename = f"{book_name}.pdf"
        HTML(string=html_content).write_pdf(pdf_filename)
        return send_file("../"+pdf_filename, as_attachment=True)

    session['purchase_book_title'] = request.form['book_title']
    session['purchase_book_id'] = request.form['book_id']
    session['purchase_book_price'] = request.form['book_price']
    session['to_where'] = request.form['to_where']
    return render_template('buying.html')