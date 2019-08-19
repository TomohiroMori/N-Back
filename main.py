from flask import Flask, render_template, request, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

times = 20

def resnumber(character_list, back, times):
    """表示される文字をtimesの数までランダムに生成し、sessionに格納。
    times+1からx+times+1(N=x) までのキーに<br>を格納し空白にする。"""
    order = random.choices(character_list, k=times)
    for i, j in enumerate(order):
        i2 = str(i+1)
        session[i2]=j
    for i in range(back):
        i2 = str(i+times+1)
        session[i2] ="<br>"


def initialization():
    """sessionの値を初期化"""
    session["times"] = 0
    session["count"] = 0
    session["order"] = 1
    session["resnum"] = 1

def routine():
    session["times"] -= 1
    session["order"] += 1
    session["resnum"] += 1
    resnum = session[str(session["resnum"])]
    return resnum


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/Try")
def Try():
    if request.args.get("n", "") and request.args.get("mode", ""):
        initialization()

        session["back"] = int(request.args.get("n", ""))
        session["mode"] = request.args.get("mode", "").split(",")
        resnumber(session["mode"], session["back"], times)

        resnum = session[str(session["resnum"])]
        return render_template('try.html', resnum=resnum)

    elif request.args.get("next", "") and session["back"] >= 1:
        """最初にN=xのx回分文字を表示。"""
        session["resnum"] += 1
        session["back"] -= 1
        if not session["back"]:
            session["times"] = times
        resnum = session[str(session["resnum"])]
        return render_template('try.html', resnum=resnum)

    elif request.args.get("sn", ""):
        """ユーザーの解答を受け取り、正誤を判定。"""
        sn = request.args.get("sn", "")
        if session[str(session["order"])] == sn:
            session["count"] += 1
            if session["order"] == times:
                rate = int((session["count"] / times) * 100)
                return render_template('index.html', rate=rate)

            resnum = routine()
            result ="〇"
            return render_template('try.html', resnum=resnum, result=result)

        elif session[str(session["order"])] != sn:
            if session["order"] == times:
                rate = int((session["count"] / times) * 100)
                return render_template('index.html', rate=rate)

            resnum = routine()
            result = "✕"
            return render_template('try.html', resnum=resnum, result=result)

    else:
        """index.htmlの項目の選択漏れを検出"""
        return render_template('index.html', error="各項目を選択してください")


if __name__ == '__main__':
    app.run(debug=True)
