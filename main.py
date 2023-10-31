from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
import pandas as pd
from backend import project

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import secrets
foo = secrets.token_urlsafe(16)

app = Flask(__name__)
app.secret_key = foo
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)
csrf.init_app(app)

class GeneratorForm(FlaskForm):
    name = StringField('Text', validators=[DataRequired(), Length(5, 20)])
    submit = SubmitField('Submit')

class SummarizerForm(FlaskForm):
    name = StringField('Text', validators=[DataRequired(), Length(10, 400)])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generator', methods=['GET', 'POST'])           
def generator():
    form = GeneratorForm()
    message = ""
    generated_text = ""
    if form.validate_on_submit():
        text = form.name.data   
    return render_template('generator.html', form=form, message=message)

@app.route('/summarizer', methods=['GET', 'POST'])
def summarizer():
    form = SummarizerForm()
    message = ""
    if form.validate_on_submit():
        text = form.data.name
        
    return render_template('summarizer.html', form=form, message=message)

@app.route('/generator-results', methods=['POST'])
def text_generator():
    text = request.form['name']
    df = pd.DataFrame({'text': [text]})
    generated_text = project.models.get('cohere_text_generation').predict(df)['next_text'][0]
    print(generated_text)
    return render_template('text.html', text=generated_text)

@app.route('/summarizer-results', methods=['POST'])
def text_summarizer():
    text = request.form['name']
    df = pd.DataFrame({'text': [text]})
    summarized_text = project.models.get('cohere_text_summarization').predict(df)['next_text'][0]
    return render_template('text.html', text=summarized_text)


if __name__ == '__main__':
    app.run(debug=True)
