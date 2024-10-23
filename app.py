from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "unaclavesecreta"


@app.route('/')
def index():
    if 'productos' not in session:
        session['productos'] = []
    return render_template('index.html', productos=session['productos'])


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
       
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        
        if cantidad < 0 or precio < 0:
           
            return "Error: La cantidad y el precio deben ser mayores o iguales a cero", 400

        descripcion = request.form['nombre']
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']

        
        nuevo_id = len(session['productos']) + 1

       
        producto = {
            'id': nuevo_id,
            'nombre': descripcion,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }

        
        session['productos'].append(producto)
        session.modified = True

        return redirect(url_for('index'))
    
    
    return render_template('agregar.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
       
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        
        if cantidad < 0 or precio < 0:
            
            return "Error: La cantidad y el precio deben ser mayores o iguales a cero", 400

       
        for producto in session['productos']:
            if producto['id'] == id:
                producto['nombre'] = request.form['nombre']
                producto['cantidad'] = cantidad
                producto['precio'] = precio
                producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
                producto['categoria'] = request.form['categoria']
                session.modified = True
                break
        return redirect(url_for('index'))
    
    
    producto = next((prod for prod in session['productos'] if prod['id'] == id), None)
    return render_template('editar.html', producto=producto)


@app.route('/eliminar/<int:id>')
def eliminar(id):
    
    session['productos'] = [prod for prod in session['productos'] if prod['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
