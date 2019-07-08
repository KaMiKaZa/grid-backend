from flask import Blueprint, current_app, request, make_response, jsonify
from pymongo import MongoClient
from bson import ObjectId
from click import echo


bp = Blueprint('database', __name__, url_prefix='/api')


@bp.route('/<string:db>/<string:coll>/create', methods = ['POST'])
def create(db, coll):
    MONGO_URI = current_app.config.get('MONGO_URI', 'mongodb://localhost:27017')

    document = request.get_json()

    with  MongoClient(MONGO_URI) as mongo:
        collection = mongo[db][coll]

        result = collection.insert_one(document)

    if result.acknowledged:
        return jsonify({ '_id': str(result.inserted_id)})
    else:
        return make_response('an error encountered while inserting', 400)


@bp.route('/<string:db>/<string:coll>/read', methods = ['GET'])
@bp.route('/<string:db>/<string:coll>/read/<int:id>')
def read(db, coll, _id = None):
    MONGO_URI = current_app.config.get('MONGO_URI', 'mongodb://localhost:27017')

    result = []

    with  MongoClient(MONGO_URI) as mongo:
        collection = mongo[db][coll]

        if _id:
            find = collection.find({ '_id': ObjectId(_id) })
        else:
            find = collection.find()

    for doc in find:
        doc['_id'] = str(doc['_id'])
        result.append(doc)

    return jsonify({
        'rows': [ r for r in result ]
    })


@bp.route('/<string:db>/<string:coll>/update', methods = ['PUT'])
def update(db, coll):
    MONGO_URI = current_app.config.get('MONGO_URI', 'mongodb://localhost:27017')

    fields = request.get_json()
    _id = fields.pop('_id')

    if not _id:
        return make_response('field "_id" must be specified for operation "update"', 400)

    with  MongoClient(MONGO_URI) as mongo:
        collection = mongo[db][coll]

        collection.update_one({ '_id': ObjectId(_id) }, { "$set": fields })

    return make_response(f'record with id "{_id}" successfully updated', 200)


@bp.route('/<string:db>/<string:coll>/delete', methods = ['DELETE'])
def delete(db, coll):
    MONGO_URI = current_app.config.get('MONGO_URI', 'mongodb://localhost:27017')

    _id = request.get_json()['_id']

    if not _id:
        return make_response('field "_id" must be specified for operation "delete"', 400)

    with  MongoClient(MONGO_URI) as mongo:
        collection = mongo[db][coll]

        collection.delete_one({ '_id': ObjectId(_id) })

    return make_response(f'record with id "{_id}" successfully deleted', 200)
