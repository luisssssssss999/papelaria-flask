from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)

def init_db():
    conn=sqlite3.connect('database.db')
    cur=conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS produtos(id INTEGER PRIMARY KEY AUTOINCREMENT,nome TEXT,categoria TEXT,quantidade INTEGER,preco REAL)')
    conn.commit(); conn.close()
init_db()

@app.route('/')
def dashboard():
    conn=sqlite3.connect('database.db'); cur=conn.cursor()
    cur.execute('SELECT COUNT(*) FROM produtos'); total=cur.fetchone()[0]
    cur.execute('SELECT COALESCE(SUM(quantidade),0) FROM produtos'); itens=cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM produtos WHERE quantidade<10'); baixo=cur.fetchone()[0]
    cur.execute('SELECT COALESCE(SUM(quantidade*preco),0) FROM produtos'); valor=cur.fetchone()[0]
    cur.execute('SELECT * FROM produtos'); produtos=cur.fetchall()
    conn.close()
    return render_template('dashboard.html',total_produtos=total,itens_estoque=itens,baixo_estoque=baixo,valor_total=valor,produtos=produtos)

@app.route('/adicionar',methods=['POST'])
def adicionar():
    conn=sqlite3.connect('database.db'); cur=conn.cursor()
    cur.execute('INSERT INTO produtos(nome,categoria,quantidade,preco) VALUES(?,?,?,?)',
    (request.form['nome'],request.form['categoria'],request.form['quantidade'],request.form['preco']))
    conn.commit(); conn.close()
    return redirect('/')

@app.route('/excluir/<int:id>')
def excluir(id):
    conn=sqlite3.connect('database.db'); cur=conn.cursor()
    cur.execute('DELETE FROM produtos WHERE id=?',(id,))
    conn.commit(); conn.close()
    return redirect('/')

app.run(debug=True)
