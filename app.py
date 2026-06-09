import os
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'devops')

mysql = MySQL(app)

def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS nps_feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(100),
                service_type VARCHAR(50),
                rating INT,
                comment TEXT,
                category VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        mysql.connection.commit()
        cur.close()

def get_category(rating):
    if rating >= 9:
        return 'Promoter'
    elif rating >= 7:
        return 'Passive'
    else:
        return 'Detractor'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT customer_name, service_type, rating, comment, category, created_at FROM nps_feedback ORDER BY created_at DESC')
    feedbacks = cur.fetchall()

    cur.execute('SELECT service_type, AVG(rating) FROM nps_feedback GROUP BY service_type')
    avg_scores = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM nps_feedback WHERE category='Promoter'")
    promoters = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM nps_feedback WHERE category='Passive'")
    passives = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM nps_feedback WHERE category='Detractor'")
    detractors = cur.fetchone()[0]

    cur.close()
    return render_template('index.html',
        feedbacks=feedbacks,
        avg_scores=avg_scores,
        promoters=promoters,
        passives=passives,
        detractors=detractors)

@app.route('/submit', methods=['POST'])
def submit():
    customer_name = request.form.get('customer_name')
    service_type = request.form.get('service_type')
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment')
    category = get_category(rating)

    cur = mysql.connection.cursor()
    cur.execute('''
        INSERT INTO nps_feedback (customer_name, service_type, rating, comment, category)
        VALUES (%s, %s, %s, %s, %s)
    ''', (customer_name, service_type, rating, comment, category))
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'success', 'category': category})

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
