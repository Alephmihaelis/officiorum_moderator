
from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'          # Servidor do MySQL
app.config['MYSQL_USER'] = 'root'               # Usuário do MySQL
app.config['MYSQL_PASSWORD'] = ''               # Senha do MySQL
app.config['MYSQL_DB'] = 'officiorum_db'        # Nome da base de dados
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Retorna dados como DICT
app.config['MYSQL_USE_UNICODE'] = True          # Usa a conversão UNICODE para caracteres
app.config['MYSQL_CHARSET'] = 'utf8mb4'         # Transações em UTF-8

mysql = MySQL(app)

@app.before_request
def before_request():
    cur = mysql.connection.cursor()
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")
    cur.execute("SET character_set_client=utf8mb4")
    cur.execute("SET character_set_results=utf8mb4")
    cur.execute("SET lc_time_names = 'pt_BR'")
    cur.close()


@app.route('/')
def home():

    action = request.args.get('ac')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `officia` WHERE status = 'pending' ORDER BY `expire`")
    tarefas = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `officia` WHERE status = 'completed'")
    tarefas_concluidas = cur.fetchall()
    cur.close()


    page = {
        'title': 'Agendador de tarefas',
        'href': '/new',
        'label': 'Cadastrar nova tarefa',
        'tarefas': tarefas,
        'tarefas_concluidas': tarefas_concluidas,
        'action': action
    }

    return render_template('home.html', page=page)

@app.route('/new', methods=['GET', 'POST'])
def new():

    created = False

    if request.method == 'POST':
        form = dict(request.form)
#      print('\n\n\n', form, '\n\n\n')
        if form['expire'] == '':
            subquery = 'DATE_ADD(NOW(), INTERVAL 30 DAY)'
        else:
            subquery = form['expire'].replace('T', ' ')

        sql = '''
            INSERT INTO officia (name, description, expire)
            VALUES (%s, %s, %s);
            '''
        cur = mysql.connection.cursor()
        cur.execute(sql, (form['name'], form['description'], subquery,))
        mysql.connection.commit()
        cur.close()

        created = True

    data_atual = datetime.now()
    data_futura = data_atual + timedelta(days=30)
    data_formatada = data_futura.strftime("%Y-%m-%d %H:%M:%S")

    page = {
        'title': 'Cadastrar nova tarefa',
        'href': '/',
        'label': 'Ver tarefas já cadastradas',
        'created': created,
        'date30': data_formatada
    }

    return render_template('new.html', page=page)

@app.route('/del/<id>')
def delete(id):

    sql = '''
        UPDATE officia
        SET status = 'deleted'
        WHERE id = %s
        '''
    
    cur = mysql.connection.cursor()
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('home', ac='del'))

@app.route('/completed/<id>')
def completed(id):

    sql = '''
        UPDATE officia
        SET status = 'completed'
        WHERE id = %s
        '''
    
    cur = mysql.connection.cursor()
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('home', ac='comp'))

@app.route('/uncheck/<id>')
def uncheck(id):

    sql = '''
        UPDATE officia
        SET status = 'pending'
        WHERE id = %s
        '''
    
    cur = mysql.connection.cursor()
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('home', ac='pen'))

@app.errorhandler(404)
def error(e):
    return e, 404

if __name__ == '__main__':
    app.run(debug=True)