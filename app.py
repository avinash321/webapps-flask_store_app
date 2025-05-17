from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    quantity = db.Column(db.Integer, default=0)

@app.route('/')
def dashboard():
    items = Item.query.all()
    return render_template('dashboard.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name'].strip()
        quantity = int(request.form['quantity'])
        if name:
            existing_item = Item.query.filter_by(name=name).first()
            if existing_item:
                existing_item.quantity += quantity
            else:
                new_item = Item(name=name, quantity=quantity)
                db.session.add(new_item)
            db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_item.html')

@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        change = int(request.form['quantity'])
        item.quantity += change
        if item.quantity <= 0:
            db.session.delete(item)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('update_item.html', item=item)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
