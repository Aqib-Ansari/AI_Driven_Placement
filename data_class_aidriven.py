import sql_functions
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TextAreaField
from wtforms.validators import InputRequired, Email, Length

class questions:
    def __init__(self,id,qtype,question,option1,option2,option3,option4,correct):
        self.id = id
        self.qtype = qtype
        self.question = question
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.option4 = option4
        self.correct = correct

question1 = questions(7,'gk','what is the fastest speed of human?','30kmph','35kmph','40kmph','20kmph',3)
question2 = questions(8,'gk','what is the fastest speed of human?','30kmph','35kmph','40kmph','20kmph',3)
question3 = questions(9,'gk','what is the fastest speed of human?','30kmph','35kmph','40kmph','20kmph',3)
question4 = questions(10,'gk','what is the fastest speed of human?','30kmph','35kmph','40kmph','20kmph',3)
question5 = questions(11,'gk','what is the fastest speed of human?','30kmph','35kmph','40kmph','20kmph',3)
question6 = questions(12,'gk','what is the fastest speed of human?','30kmph','35kmph','40kmph','20kmph',3)
questions_list = (question2,question3,question4,question5,question6)

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    middlename = StringField('Middle Name')
    age = IntegerField('Age', validators=[InputRequired()])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[InputRequired()])
    phone = StringField('Phone Number', validators=[InputRequired(),Length(10)])
    year = StringField('Year', validators=[InputRequired()])
    course = StringField('Course', validators=[InputRequired()])
    college = StringField('College', validators=[InputRequired()])
    rollno = StringField('Roll Number', validators=[InputRequired()])
    

if __name__ == "__main__":

    # print(question1.id)
    # for q in questions_list:
    #     sql_functions.insert_question(q)
    #     print(q.id)
    sql_functions.insert_question(question1)
