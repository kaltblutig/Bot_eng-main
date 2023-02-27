active_users_interview = {} 

interview_passed_score = 7

interivew_python_questions = [
    "Tell me about yourself and your development experience.",
    "Have you ever learned any other programming language and why?",
    "Is Python case sensitive?",
    "What data types do you know?",
    "What is a Lambda function?",
    "What is a difference between shallow and deep copying?",
    "What do you know about OOP and its principles?",         # ниже практика
    "Write a program to produce Fibonacci series in Python.", 
    "Write a program in Python to check if a number is prime.",
    "Write a function to reverse a string."
]

interview_dct = {
    'start_message': '''Are you ready? Let's start! Today we will have an interview on Python developer position. 
                        We will ask you various questions about Python and check your answers. 
                        After each question, we will correct you a little in Python itself.
                        If you're asked to write a code -- send a code :)
                        ATTENTION: send one message as an answer for each question only!
                        
                        If you want to go to the next question, type command "/next".
                            
                        We hope that this simulator will help you better prepare for an interview, to learn Python and English.''',

    'restart_message': 'If you would like to try again, type command "/start". Good luck!',

    'go_to_next': 'If you want to go to the next question type command "/next". Till that your phrases are related to the last question given.'
}