from flask import Flask, render_template, jsonify, request
import pymysql

app = Flask(__name__)
db = pymysql.connect(host='localhost', port=3306, user='berry', passwd='1234', db='web_test', charset="utf8")
cursor = db.cursor()

@app.route('/', methods=["GET"])
def main_page():
    return render_template('index.html')

@app.route('/students', methods=["GET"])
def get_students():
    sql = """
    SELECT * FROM student_score
    """
    cursor.execute(sql)
    students = cursor.fetchall()
    student_list = []
    for student in students :
        student_list.append({
            "name": student[1],
            "korean": student[2],
            "math": student[3],
            "english": student[4]
        })
    return jsonify(student_list)

@app.route('/student', methods=["POST"])
def add_student():
    name = request.form["name"]
    korean = request.form["korean"]
    math = request.form["math"]
    english = request.form["english"]
    sql = """
    INSERT INTO student_score (name, korean, math, english) VALUES ('%s', %s, %s, %s)
    """ % (name, korean, math, english)
    cursor.execute(sql)
    db.commit()
    return "OK"

@app.route("/student", methods=["PUT"])
def update_student():
    name = request.form["name"]
    korean = request.form["korean"]
    math = request.form["math"]
    english = request.form["english"]
    sql = """
        UPDATE student_score SET korean=%s, math=%s, english=%s where name = '%s'
    """ % (korean, math, english, name)
    cursor.execute(sql)
    db.commit()
    return "OK"

@app.route("/student", methods=["DELETE"])
def delete_student():
    name = request.args.get("name")
    sql = """
        DELETE FROM student_score where name = '%s'
    """ % (name)
    cursor.execute(sql)
    db.commit()
    return "OK"


if __name__ == '__main__':
    app.run()
