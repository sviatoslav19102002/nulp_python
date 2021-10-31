__version__ = '0.1.0'

#from flask import Flask
import flask
from flask import Flask, request, Response, jsonify
from flask_bcrypt import Bcrypt
import sys
sys.path.append('/Users/orestchukla/Desktop/sviatproject/nulp_python/poetry-demo/Migrations')
from main import Session, User, Wallet, Transfer
sys.path.append('/Users/orestchukla/Desktop/sviatproject/nulp_python/poetry-demo/poetry_demo')
from validation_check import UserSchema, WalletSchema, TransferSchema
from waitress import serve
from marshmallow import ValidationError
app = Flask(__name__)
session = Session()
bcrypt = Bcrypt()


@app.route('/api/v1/hello-world-15')
def myendpoint():
    status_code = flask.Response(status=200, response="Hello World 15")
    return status_code


@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if user already exists
    exists = session.query(User.id).filter_by(username=data['username']).first()
    exists2 = session.query(User.id).filter_by(email=data['email']).first()
    if exists or exists2:
        return Response(status=400, response='User with such username or email already exists.')

    # Hash user's password
    hashed_password = bcrypt.generate_password_hash(data['password'])
    # Create new user
    new_user = User(first_name=data['first_name'], second_name=data['second_name'], username=data['username'], password=hashed_password, email=data['email'])

    # Add new user to db
    session.add(new_user)
    session.commit()

    return Response(response='New user was successfully created!')


@app.route('/api/v1/user/<username>', methods=['GET'])
def get_user(username):
    # Check if user exists
    db_user = session.query(User).filter_by(username=username).first()
    if not db_user:
        return Response(status=404, response='A user with provided username was not found.')

    # Return user data
    user_data = {'id': db_user.id, 'first_name': db_user.first_name, 'second_name': db_user.second_name, 'username': db_user.username, 'email': db_user.email}
    return jsonify({"user": user_data})


@app.route('/api/v1/user/<username>', methods=['PUT'])
def update_user(username):
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if wallet exists
    db_user = session.query(User).filter_by(username=username).first()
    if not db_user:
        return Response(status=404, response='A user with provided username was not found.')

    # Check if username or email is not taken if user tries to change it
    if 'username' in data.keys() and db_user.username != data['username']:
        exists = session.query(User.id).filter_by(username=data['username']).first()
        if exists:
            return Response(status=400, response='User with such username already exists.')
    if 'email' in data.keys() and db_user.email != data['email']:
        exists2 = session.query(User.id).filter_by(email=data['email']).first()
        if exists2:
            return Response(status=400, response='User with such email already exists.')
    # Change user data
    if 'first_name' in data.keys():
        db_user.first_name = data['first_name']
    if 'second_name' in data.keys():
        db_user.second_name = data['second_name']
    if 'password' in data.keys():
        hashed_password = bcrypt.generate_password_hash(data['password'])
        db_user.password = hashed_password
    if 'username' in data.keys():
        db_user.username = data['username']
    if 'email' in data.keys():
        db_user.email = data['email']

    # Save changes
    session.commit()

    # Return new user data
    user_data = {'id': db_user.id, 'first_name': db_user.first_name, 'second_name': db_user.second_name, 'username': db_user.username, 'email': db_user.email}
    return jsonify({"user": user_data})


@app.route('/api/v1/user/<username>', methods=['DELETE'])
def delete_user(username):
    # Check if user exists
    db_user = session.query(User).filter_by(username=username).first()
    if not db_user:
        return Response(status=404, response='A user with provided username was not found.')

    # Delete user
    session.delete(db_user)
    session.commit()
    return Response(response='User was deleted.')


@app.route('/api/v1/wallet', methods=['POST'])
def create_wallet():
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        WalletSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if wallet already exists
    exists = session.query(Wallet.id).filter_by(name=data['name']).first()
    if exists:
        return Response(status=400, response='Wallet with such name already exists.')

    # Check if username already exists
    exists2 = session.query(User.id).filter_by(id=data['owner_id']).first()
    if not exists2:
        return Response(status=400, response='There is not user with such ID.')
    new_wallet = Wallet(name=data['name'], amount=0, owner_id=data['owner_id'])

    # Check if user already has wallet
    exists = session.query(Wallet.id).filter_by(name=data['name']).first()


    # Add new wallet to db
    session.add(new_wallet)
    session.commit()

    return Response(response='New wallet was successfully created!')


@app.route('/api/v1/wallet/<name>', methods=['GET'])
def get_wallet(name):
    # Check if wallet exists
    db_wallet = session.query(Wallet).filter_by(name=name).first()
    if not db_wallet:
        return Response(status=404, response='A wallet with provided name was not found.')

    # Return wallet data
    db_user = session.query(User).filter_by(id=db_wallet.owner_id).first()
    wallet_data = {'id': db_wallet.id, 'name': db_wallet.name, 'amount': db_wallet.amount, 'owner_username': db_user.username}
    return jsonify({"user": wallet_data})


@app.route('/api/v1/wallet/<name>', methods=['PUT'])
def update_wallet(name):
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        WalletSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if wallet exists
    db_wallet = session.query(Wallet).filter_by(name=name).first()
    if not db_wallet:
        return Response(status=404, response='A wallet with provided name was not found.')

    # Check if name of wallet is not taken if user tries to change it
    if 'name' in data.keys() and db_wallet.name != data['name']:
        exists = session.query(Wallet.id).filter_by(name=data['name']).first()
        if exists:
            return Response(status=400, response='Wallet with such name already exists.')
    # Change wallet data
    if 'owner_id' in data.keys() and db_wallet.owner_id != data['owner_id']:
        exists2 = session.query(User.id).filter_by(id=data['owner_id']).first()
        if not exists2:
            return Response(status=400, response='There is not user with such ID.')
    if 'name' in data.keys():
        db_wallet.name = data['name']
    if 'owner_id' in data.keys():
        db_wallet.owner_id = data['owner_id']

    # Save changes
    session.commit()

    # Return new wallet data
    db_user = session.query(User).filter_by(id=db_wallet.owner_id).first()
    wallet_data = {'id': db_wallet.id, 'name': db_wallet.name, 'owner_username': db_user.username}
    return jsonify({"wallet": wallet_data})


@app.route('/api/v1/wallet/<name>', methods=['DELETE'])
def delete_wallet(name):
    # Check if wallet exists
    db_wallet = session.query(Wallet).filter_by(name=name).first()
    if not db_wallet:
        return Response(status=404, response='A wallet with provided name was not found.')

    # Delete wallet
    session.delete(db_wallet)
    session.commit()
    return Response(response='Wallet was deleted.')


@app.route('/api/v1/transfer', methods=['POST'])
def create_transfer():
    data = request.get_json()

    # Validate input data
    try:
        TransferSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if from and to wallets are not the same
    if data['fr0m_id'] == data['to_id']:
        return Response(status=400, response='You can not send money to the same wallet.')

    # Check if wallets exists
    wallet_from = session.query(Wallet).filter_by(id=data['fr0m_id']).first()
    wallet_to = session.query(Wallet).filter_by(id=data['to_id']).first()
    if not wallet_from or not wallet_to:
        return Response(status=400, response='Wallet with such id does not exist.')

    if data['amount'] > wallet_from.amount:
        return Response(status=400, response='There is not necessary amount of money.')

    # Create new transfer
    new_user = Transfer(purpose=data['purpose'], amount=data['amount'], fr0m_id=data['fr0m_id'], to_id=data['to_id'])

    # Add new transfer to db
    session.add(new_user)

    wallet_from.amount -= data['amount']
    wallet_to.amount += data['amount']

    session.commit()

    return Response(response='New transfer was successfully created!')


serve(app, host='0.0.0.0', port=8080, threads=1) #WAITRESS!


