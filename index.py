from flask import Flask, render_template, request
import subprocess
from threading import Timer
app = Flask(__name__)
@app.route("/",methods = ['GET', 'POST'])
def home():
    # Check if we get a post
    if request.method == 'POST':
        #Get the command
        try:
            command=request.form['command']
            dangerous=["rm",":&}","command","mv","wget","Mkfs",">","^","dd","su","sudo","*","bash","zsh","chmod","sh","ssh","bin","cat"]
            for danger in dangerous:
                if (danger in command):
                      return render_template("home.html", output="We caught you doing something stupid and dangerous! <br/> Don't do it again or else ...")

            kill = lambda process: process.kill()
            print(command.split())
            output=subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            my_timer = Timer(0.01, kill, [output])
            try:
                my_timer.start()
                stdout, stderr = output.communicate()
            finally:
                my_timer.cancel()
            print(stdout)
            output=stdout + stderr  
            output=output.decode('utf-8')
            output=output.split("\n")[::-1]
            final=""
            for a in output:
                final+=a+"<br/>"

            return render_template("home.html", output=final)
        except Exception:
            return render_template("home.html", output="Command Failed :)")
    else:
        return render_template("home.html")
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
