import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.2'
port = 8001

server.bind((ip_address, port))
server.listen()

clients = []

questions = ["Which CPU powered the Altair 8800? \n a.Atmel-ATMEGA328p \n b.Intel-8080 c.Intel-4004 \n d.AMD-AM9080", 
            "A camel's hump is for: \n a.Storing water \n b.Deterring predators \n c.Storing fat \n d.Providing balance",
            "Which of these dogs are used pull sleds? \n a.Huskies \n b.Golden Retrievers \n c.Chihuahuas \n d.Terriers",
            "The ENIAC used ____ instead of transistors: \n a.Mechanical Relays \n b.manual switches \n c.Variable resistors \n d.Vacuum Tubes"]

answers = ["b", "c", "a", "d"]

print("Server has started...")


def get(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn):
    score = 0
    conn.send("Welcome to the quiz!".encode('utf-8'))
    conn.send("Each question is multiple choice. You may pick any answer out of A, B, C or D.\n".encode('utf-8'))
    conn.send("There is only one correct answer per question.\n\n".encode('utf-8'))
    index, question, answer = get(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Correct! Score: {score}\n\n".encode('utf-8'))
                else:
                    conn.send(f"Incorrect! Score: {score}\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get(conn)
            else:
                remove(conn)
        except:
            continue

def remove(connection):
    if connection in clients:
        clients.remove(connection)

while True:
    conn, addr = server.accept()
    clients.append(conn)
    print (addr[0] + " connected")
    new_thread = Thread(target= clientthread,args=(conn))
    new_thread.start()
    
