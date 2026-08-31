from flask import Flask
import datetime

app = Flask(__name__)

@app.route("/")
def index():
      now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      return "个人练习 " 

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)