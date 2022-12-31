"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "hijklmnop"

connect_db(app)
app.app_context().push()


@app.route('/api/cupcakes')
def list_cupcakes():
    """List all cupcakes in the database."""

    all = Cupcake.query.all()
    cupcakes = [cupcake.serialize() for cupcake in all]
    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:cupcake_id>')
def show_cupcake(cupcake_id):
    """Return data on a specific cupcake with the given id"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake and return data about the new cupcake"""

    cupcake = Cupcake(
        flavor=request.json['flavor'],
        rating=request.json['rating'],
        size=request.json['size'],
        image=request.json['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update information about the cupcake of a given id"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json['flavor']
    cupcake.rating = request.json['rating']
    cupcake.size = request.json['size']
    cupcake.image = request.json['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete cupcake of a given id"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='Deleted')


@app.route('/')
def homepage():
    """Render homepage"""

    return render_template('index.html')
