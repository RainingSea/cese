from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class Main:
    def __init__(self):
        self.users_file = 'users.txt'
        self.medical_info_file = 'medical_info.txt'
        self.reminders_file = 'reminders.txt'
        self.load_data()

    def load_data(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users[username] = password

    def main(self):
        return redirect(url_for('login'))

    def register_user(self, username: str, password: str):
        if username not in self.users:
            self.users[username] = password
            with open(self.users_file, 'a') as file:
                file.write(f"{username},{password}\n")

    def login_user(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def add_medical_info(self, username: str, info: str):
        with open(self.medical_info_file, 'a') as file:
            file.write(f"{username}|{info}\n")

    def set_reminder(self, username: str, reminder: str):
        with open(self.reminders_file, 'a') as file:
            file.write(f"{username}|{reminder}\n")

main_instance = Main()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        main_instance.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/medical_info', methods=['GET', 'POST'])
def medical_info():
    if request.method == 'POST':
        username = request.form['username']
        info = request.form['info']
        main_instance.add_medical_info(username, info)
    return render_template('medical_info.html')

@app.route('/reminders', methods=['GET', 'POST'])
def reminders():
    if request.method == 'POST':
        username = request.form['username']
        reminder = request.form['reminder']
        main_instance.set_reminder(username, reminder)
    return render_template('reminders.html')

if __name__ == '__main__':
    app.run(port=8179, debug=False)
