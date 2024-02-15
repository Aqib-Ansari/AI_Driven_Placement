import google.generativeai as genai

# Used to securely store 



GOOGLE_API_KEY="AIzaSyDn3LTVkTF8oI6-3Z40Ax8X_nka6gfhnLg"

genai.configure(api_key=GOOGLE_API_KEY)




model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def start_interview():
    response =chat.send_message("introduce your self as a 'Ai interviewer' and ask the candidate his name and how he is. do not ask any question ")
    print(response.text)
    print("\n\n"+"___________________________________________"*3 + "\n\n")
    return response.text

def interview_process():
    for i in range(3):
        
        question_query =chat.send_message("Ask me only 1 easy python interview question")
        print(question_query.text)
        answer = input("\n Enter Answer : \n")
        answer_query = chat.send_message(answer)
        print(answer_query.text)
        print("\n\n"+"___________________________________________"*3 + "\n\n")


def end_interview():
    response =chat.send_message("Tell me how many answers were correct for the above three questions, also give me some feedback")
    print(response.text)
    return response.text




if __name__ == "__main__":
    start_interview()
    interview_process()
    end_interview()
