from flask import Flask, render_template, request, redirect
from clinicapp.app import app

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template ('login.html')


@app.route('/signup')
def signup():
    return render_template ('signup.html')


@app.route('/datlichkham')
def datlichkham():
    return render_template('datlichkham.html')


@app.route('/lapphieukham')
def lapphieukham():
    return render_template('lapphieukham.html')


@app.route('/baocaothongke')
def baocaothongke():
    return render_template('baocaothongke.html')


@app.route('/thanhtoan')
def thanhtoan():
     return render_template('thanhtoan.html')


if __name__ == '__main__':
    app.run(debug=True)