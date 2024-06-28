from flask import Flask
from flask import render_template, redirect, url_for,request, Response, session, flash, g
from flask_mysqldb import MySQL, MySQLdb
from datetime import datetime
from config import config
from dateutil.relativedelta import relativedelta
from functools import wraps


app = Flask(__name__,template_folder='templates')

class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'parkhouse'
    MYSQL_CURSORCLASS = 'DictCursor'

config = {
    'development': DevelopmentConfig
}

app.config.from_object(config['development'])

db= MySQL(app)

'''
def login_required(role_id):
    def wrapper(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'loggedin' not in session or session['role_id'] != role_id:
                return redirect('/')
            return func(*args, **kwargs)
        return decorated_function
    return wrapper
'''
@app.before_request
def before_request():
    # La función get_logged_in_user() obtiene el usuario actual de la sesión
    g.user = get_logged_in_user()

def get_logged_in_user():
    user_id = session.get('user_id')
    if user_id:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
        user = cur.fetchone()
        cur.close()
        return user
    return None

@app.route('/')
def index():
    return render_template('login.html')
'''
@app.route('/admin',  methods=["GET", "POST"])
@login_required(role_id=1)
def admin():
    session['user_data'] = session.get('user_data') or {}
    return redirect(url_for('inventario', role='admin'))

@app.route('/visor')
#@login_required(role_id=3)
def visor():
    session['user_data'] = session.get('user_data') or {}
    return redirect(url_for('home', role='visor'))

@app.route('/editor')
#@login_required(role_id=2)
def editor():
    session['user_data'] = session.get('user_data') or {}
    return redirect(url_for('inventario', role='editor'))'''

@app.route('/access-login', methods=["GET", "POST"])
def login():

    if request.method == "POST" and 'inputUsername' in request.form and 'inputPassword' in request.form:
        username = request.form['inputUsername']
        password = request.form['inputPassword']

        cur = db.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        account = cur.fetchone()

        if account:
            session['loggedin'] = True
            session['user_id'] = account['user_id']
            session['role_id'] = account['role_id']
            session['first_name'] = account['first_name']
            session['last_name'] = account['last_name']
            session['username'] = account['username']

            if session['role_id'] == 1:
                return redirect(url_for('show_prod'))
            
            elif session['role_id'] == 2:
                return redirect(url_for('show_prod'))
            
            elif session['role_id'] == 3:
                return redirect(url_for('home'))
        else:
            return render_template('login.html', mensaje="Usuario o contraseña incorrecta")
    return redirect('/')

#cerrar sesion
'''@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')'''
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', first_name=session['first_name'])
    else:
        return redirect(url_for('login'))

@app.route('/registro')
def registro():
    if 'username' in session:
        cur = db.connection.cursor()
        cur.execute(f'''SELECT * FROM roles''')
        roles = cur.fetchall()
        cur.close()
        return render_template('register.html', first_name=session['first_name'], roles=roles)
    else:
        return redirect(url_for('login'))

@app.route('/registro_prod')
def registro_prod():
    if 'username' in session:
        cur = db.connection.cursor()
        cur.execute(f'''SELECT * FROM roles''')
        roles = cur.fetchall()
        cur.close()
        return render_template('register_prod.html', first_name=session['first_name'], roles=roles)
    else:
        return redirect(url_for('login'))

#MOSTRAR PRODUCTOS
@app.route('/inventario')
def show_prod():
    if 'username' in session:
        sort_by = request.args.get('sort_by')
        if sort_by:
            if sort_by == 'nombre':
                order_by_clause = 'ORDER BY name_prod'
            elif sort_by == 'descripcion':
                order_by_clause = 'ORDER BY desc_prod'
            elif sort_by == 'precio':
                order_by_clause = 'ORDER BY price'
            elif sort_by == 'proveedor':
                order_by_clause = 'ORDER BY supplier'
            elif sort_by == 'categoria':
                order_by_clause = 'ORDER BY category'
            elif sort_by == 'stock':
                order_by_clause = 'ORDER BY stock'

            # Realiza la consulta a la base de datos para obtener los productos ordenados
            cur = db.connection.cursor()
            cur.execute(f'''SELECT p.*, c.cat_name AS categoria_nombre
                    FROM products p
                    LEFT JOIN categories c ON p.category = c.cat_id {order_by_clause}''')
            productos = cur.fetchall()
            cur.close()
            return render_template('inventario.html', first_name=session['first_name'],productos=productos, categorias=categorias)

        
        cur = db.connection.cursor()
        cur.execute('''SELECT p.*, c.cat_name as categ_name, c.cat_id as id_categ, s.supp_name as name_supplier, s.supp_id as id_supplier
        FROM products p
        LEFT JOIN categories c ON p.category = c.cat_id
        LEFT JOIN supplier s ON p.supplier = s.supp_id''')
        productos = cur.fetchall()

        #Obtiene categorias
        cur = db.connection.cursor()
        cur.execute('''SELECT * FROM categories''')
        categorias = cur.fetchall()

        #Obtiene Proveedores
        cur = db.connection.cursor()
        cur.execute('''SELECT * FROM supplier''')
        proveedor = cur.fetchall()
        cur.close()
        
        return render_template('inventario.html', first_name=session['first_name'],productos=productos, categorias=categorias, proveedor=proveedor)
    else:
        return redirect(url_for('login'))


#MOSTRAR USUARIOS
@app.route('/users', methods=["GET", "POST"])
def show_users():

    if 'username' in session:
        
        cur = db.connection.cursor()
        cur.execute('''SELECT u.*, r.name as rol_name, r.role_id
                    FROM users u
                    LEFT JOIN roles r ON u.role_id = r.role_id''')
        usuarios = cur.fetchall()

        cur = db.connection.cursor()
        cur.execute('SELECT * FROM roles')
        roles = cur.fetchall()
        cur.close()
        return render_template('users.html', first_name=session['first_name'],usuarios=usuarios, roles=roles)
    else:
        return redirect(url_for('login'))


#Registro usuarios
@app.route('/add_user', methods=["POST"])
#@login_required(role_id=1) 
def add_user():
    if request.method == "POST":
        if request.method == 'POST':
            if 'id_rol' not in request.form:
                flash('El campo "Rol" es obligatorio.', 'danger')
                return render_template('register.html')
            
            role_id = request.form['id_rol']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            password = ['']
            run = request.form['run']
            dv = request.form['dv']

            # Verificar si se han dejado campos en blanco
            if not first_name or not last_name or not run or not dv:
                flash('Por favor, completa todos los campos.', 'danger')
                return render_template('register.html')
        

            #Creacion del nombre de usuario con 3 primeras letras del nombre y apellido completo
            username = f"{first_name[:3].lower()}.{last_name.lower()}"
            
            cur = db.connection.cursor()
            cur.execute('INSERT INTO users(role_id, username, run, dv, password, first_name, last_name) VALUES(%s,%s,%s,%s,%s,%s,%s)',
                        (role_id,username,password,first_name, last_name, run,dv))
            db.connection.commit()
            cur.close()

            flash('Usuario creado!', 'success')
            return redirect(url_for('registro'))
        return redirect(url_for('registro'))


@app.route('/list_cat')
def list_cat():
    cur = db.connection.cursor()
    query = "SELECT cat_id, cat_name FROM categories"
    cur.execute(query)
    categories = cur.fetchall()
    cur.close()
    return render_template('register_prod.html', categories=categories)

#Agregar producto
@app.route('/add_product', methods=['GET', 'POST'])
#@login_required(role_id=2) 
def add_product():
    if request.method == 'POST':
            if 'category' not in request.form:
                flash('Seleccione opcion en el campo "Categoria".', 'danger')
                return redirect(url_for('show_prod'))

            '''if 'addImg' not in request.files:
                flash('Agrege una imagen')
                return redirect(url_for('show_prod'))'''

            name = request.form['name']
            desc = request.form['desc']
            price = request.form['price']
            supplier = request.form['supplier']
            stock = request.form['stock']
            category = request.form['category']
            #img = request.files['addImg']

            # Verificar si se han dejado campos en blanco
            if not name or not desc or not price or not stock:
                flash('Por favor, completa todos los campos.', 'danger')
                return redirect(url_for('show_prod'))

            # Verificar si el supplier_id existe en la tabla supplier
            cur = db.connection.cursor()
            # cur.execute("SELECT supp_id FROM supplier WHERE supp_id = %s", (supplier,))
            
            cur = db.connection.cursor()
            cur.execute('INSERT INTO products(name_prod, desc_prod, price, supplier, category, stock) VALUES(%s,%s,%s,%s,%s,%s)',
                        (name,desc,price, supplier, category,stock))
            db.connection.commit()
            cur.close()

            flash('Producto agregado!')
            return redirect(url_for('show_prod'))
    
    return redirect(url_for('show_prod'))


#Editar producto
@app.route('/edit_product/<int:id>', methods=['POST'])
#@login_required(role_id=2) 
def edit_product(id):

            name = request.form['editName']
            desc = request.form['editDesc']
            price = request.form['editPrice']
            supplier = request.form['editSupplier']
            category = request.form['editCategory']
            stock = request.form['editStock']
            #img = request.form['editImg']
  
            
            #Obtiene usuario actual
            user_id = session['user_id']
            first_name = session['first_name']
            last_name = session['last_name']

            #Actualizar productos
            cur = db.connection.cursor()
            cur.execute('UPDATE products SET name_prod = %s, desc_prod = %s, price = %s, supplier = %s, category = %s,stock = %s WHERE prod_id = %s',
                    (name, desc, price, supplier, category, stock, id))
            db.connection.commit()
            cur.close()

            #Insertar datos en la tabla modificaciones
            cur = db.connection.cursor()
            cur.execute('INSERT INTO modifications (id_prod, id_user, first_name, last_name) VALUES(%s,%s,%s,%s)', 
                        (id, user_id, first_name,last_name))
            db.connection.commit()
            cur.close()

            flash('Producto Modificado!')
            return redirect(url_for('show_prod'))

# EDITAR USUARIOS POR PARTE DEL ADMIN
@app.route('/edit_user/<int:user_id>', methods=["POST"])
#@login_required(role_id=1)  
def edit_user(user_id):
    if request.method == "POST":
        id_rol = request.form['editIdRol']
        username = request.form['editUsername']
        first_name = request.form['editName']
        last_name = request.form['editLastName']
        run = request.form['editRut']
        dvrun = request.form['editDvRut']

        #Generar nueva contraseña
        generate_password_flag = request.form.get('generatePassword')
        if generate_password_flag:
            password = generate_password()
            cur = db.connection.cursor()
            cur.execute('UPDATE users SET role_id = %s, username = %s, first_name = %s, last_name = %s, run = %s, dvrun = %s, password = %s WHERE user_id = %s',
                    (id_rol, username, first_name, last_name, run, dvrun, password, user_id))
        else:
            cur = db.connection.cursor()
            cur.execute('UPDATE users SET role_id = %s, username = %s, first_name = %s, last_name = %s, run = %s, dvrun = %s WHERE user_id = %s',
                (id_rol, username, first_name, last_name, run, dvrun, user_id))
            
        db.connection.commit()
        cur.close()

        flash(f'Usuario {first_name} Modificado!')
        return redirect(url_for('show_users'))

# ELIMINAR USUARIOS POR PARTE DEL ADMIN
@app.route('/delete_user/<int:user_id>', methods=["POST"])
#@login_required(role_id=1)  
def delete_user(user_id):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    db.connection.commit()
    cur.close()
    return redirect('/users')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
