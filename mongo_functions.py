import pymongo
import encryption_func
client = pymongo.MongoClient("mongodb+srv://aidriven:root_aidriven@aidriven.zuyo5fq.mongodb.net/?retryWrites=true&w=majority")

if client:
    print("connected to mongodb")

def register_student(student):
    aidriven  =  client["aidriven"]
    student_register = aidriven['student_register']
    result = student_register.insert_one(student)
    return result


student1 = {
        "username":"aqib",
        "email"   :"aqibansari22298@gmail.com",
        "password":f"{encryption_func.encrypt_password('Aqib@22298')}",
        "Enrolno" : "A2020113704",
        "college":"KC college",
        "course":"BSC CS",
        "year":"FY",
        "rollno":123
    }

print(register_student(student=student1))