from flask import Flask
import datetime

app = Flask(__name__)

@app.route("/")
def index():
      now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      return "你好！服务器当前时间是 " + now

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)