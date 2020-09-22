from flask import Flask, render_template
import flask
import json
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, RadioField
from flask_wtf.csrf import CSRFProtect
from wtforms.validators import DataRequired, email_validator,Required
import random

app = Flask(__name__)

app.config['SECRET_KEY'] = "secretkey"
app.config['WTF_CSRF_SECRET_KEY'] = "secretkey"


goals_ = {"travel": "Для путешествий", "study": "Для учебы", "work": "Для работы", "relocate": "Для переезда"}
times={ "12":"1-2 часа в неделю","35":"3-5 часов в неделю","57":"5-7 часов в неделю","710":"7-10 часов в неделю"}
week={"mon":"Понедельник","tue":"Вторник","wed":"Среда","thu":"Четверг","fri":"Пятница","sat":"Суббота","sun":"Воскресенье"}

def save_request(dict_request,filename):
    requests=[] 
    try:  
        with open(filename, "r",encoding='utf-8') as f:
            requests = json.load(f)
    except:
        requests=[]      
    requests.append(dict_request)
    try:
        with open(filename, "w",encoding='utf-8') as f:
            json.dump(requests, f,ensure_ascii=False)
            return True
    except:
        return False

def check_new_goals(teachers,goals):
    goals_ch={}
    for t in teachers:
        for key  in t['goals']:
            if key not in goals_ch:
                goals_ch[key]= key 


    new_goals={}
    for key, value in goals_ch.items():
        if key in goals:
            new_goals[key]=goals[key]
        else:
            new_goals[key]=goals_ch[key]

    return new_goals



with open("data.json", "r",encoding='utf-8') as f:
    teachers = json.load(f)

goals=check_new_goals(teachers,goals_)






class RequestForm(FlaskForm):
    time_list=[ (key,value) for key,value in times.items()]
    choices_list= [(key,value)  for key,value in goals.items()]
    name = StringField('Вас зовут', validators=[DataRequired()])
    phone = StringField('Ваш телефон',validators=[DataRequired()])
    goal=RadioField('Какая цель занятий?', choices=choices_list, default=choices_list[0][0])
    time=RadioField('Сколько времени есть?', choices= time_list, default=time_list[0][0])
    submit = SubmitField('Найдите мне преподавателя')

class RequestBooking(FlaskForm):
    clientWeekday=StringField(validators=[DataRequired()])
    clientTime=StringField(validators=[DataRequired()])
    clientTeacher=StringField(validators=[DataRequired()])
    clientName = StringField('Вас зовут', validators=[DataRequired()])
    clientPhone = StringField('Ваш телефон',validators=[DataRequired()])
    submit = SubmitField('Записаться на пробный урок')



@app.route('/')
def main():
    r=[]
    while len(r)<6: 
        n=random.randint(0, 11) 
        if n not in r :
            r.append(n)
    return render_template('index.html',teachers=teachers, goals=goals,ran=r)


@app.route('/request/')
def render_myform():
    form = RequestForm()
    return render_template('request.html', form=form)

@app.route('/request_done/', methods=['POST'])
def render_request_done():
    goal=goals[flask.request.form.get('goal')]
    time=times[flask.request.form.get('time')]
    name=flask.request.form.get('name')
    phone=flask.request.form.get('phone')

    dict_request={}
    dict_request["goal"]=goal
    dict_request["time"]=time
    dict_request["name"]=name
    dict_request["phone"]=phone

    if save_request(dict_request,'request.json'):
        return render_template('request_done.html', name=name,goal=goal,time=time, phone=phone)
    else:
        print("Error- request not save.")

@app.route('/goal/<id>/')
def render_goal(id):
    goal=id
    s=[]
    for t in teachers:
        if goal in t['goals']:
            s.append(t)
    newlist = sorted(s, key=lambda k: k['rating'],reverse=True) 
    return render_template('goal.html',teachers=newlist,goal=goals[id])

 
@app.route('/profile/<int:id>/')
def render_profile(id):
    teacher=teachers[id]
    list_goals=[]
    for key in teacher["goals"]:
        list_goals.append(goals[key])
    return render_template('profile.html',teacher=teacher,id=id,list_goals=("; ".join(list_goals)))

@app.route('/booking/<int:id>/<day>/<time>/')
def render_booking(id,day,time):
    form=RequestBooking()
    teacher=teachers[id]
    list_goals=[]
    t=week[day]+" "+time[:-2]+":"+time[2:]
    for key in teacher["goals"]:
        list_goals.append(goals[key])
    return render_template('booking.html',teacher=teacher,timestring=t,form=form,id=id,day=day,time=time[:-2]+":"+time[2:])    

@app.route('/booking_done/', methods=['POST'])
def render_booking_done():
    dict_request={}
    dict_request["clientTeacher"]=flask.request.form.get('clientTeacher')
    dict_request["clientTime"]=flask.request.form.get('clientTime')
    dict_request["clientWeekday"]=flask.request.form.get('clientWeekday')
    dict_request["clientName"]=flask.request.form.get('clientName')
    dict_request["clientPhone"]=flask.request.form.get('clientPhone')
    time=flask.request.form.get('timestring')

    if save_request(dict_request,'booking.json'):
        return render_template('booking_done.html', name=flask.request.form.get('clientName'),time=time, phone=flask.request.form.get('clientPhone'))
    else:
        print("Error- request not save.")
# app.run(debug=True)
if __name__ == '__main__':
    app.run()
