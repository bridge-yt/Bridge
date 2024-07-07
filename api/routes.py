from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from .models import Resource
from . import db
import logging
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, BadRequest

bp = Blueprint('api', __name__, url_prefix='/api')
logging.basicConfig(level=logging.INFO)

# Marshmallow Schema for Resource
class ResourceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    arn = fields.Str(required=True)
    value = fields.Str(allow_none=True)
    resource_type = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

resource_schema = ResourceSchema()
resources_schema = ResourceSchema(many=True)

@bp.route('/resource', methods=['POST'])
def add_resource():
    data = request.get_json()
    logging.info(f"POST /resource data: {data}")

    try:
        resource_schema.load(data)
        if Resource.query.filter_by(name=data['name']).first():
            logging.info("Resource with this name already exists")
            return jsonify({'error': 'Resource with this name already exists'}), 409

        resource = Resource(**data)
        db.session.add(resource)
        db.session.commit()
        logging.info(f"Resource created: {resource}")

        return resource_schema.jsonify(resource), 201
    except ValidationError as ve:
        logging.error(f"ValidationError: {ve.messages}")
        return jsonify({'error': 'Invalid data', 'messages': ve.messages}), 400
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        db.session.rollback()
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        logging.error(f"Exception: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

@bp.route('/resource/<name>', methods=['GET'])
def get_resource(name):
    logging.info(f"GET /resource/{name}")
    resource = Resource.query.filter_by(name=name).first_or_404()
    logging.info(f"Resource found: {resource}")
    return resource_schema.jsonify(resource), 200

@bp.route('/resource/all', methods=['GET'])
def get_all_resources():
    logging.info("GET /resource/all")
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    resources_pagination = Resource.query.paginate(page, per_page, error_out=False)
    resources = resources_pagination.items
    total = resources_pagination.total

    logging.info(f"Resources list: {resources}")
    response = {
        'total': total,
        'page': page,
        'per_page': per_page,
        'resources': resources_schema.dump(resources)
    }
    return jsonify(response), 200

@bp.route('/resource/<name>', methods=['PUT'])
def update_resource(name):
    data = request.get_json()
    logging.info(f"PUT /resource/{name} data: {data}")

    try:
        resource_schema.load(data)
        resource = Resource.query.filter_by(name=name).first()
        if not resource:
            raise NotFound(f'Resource with name {name} does not exist')

        resource.arn = data['arn']
        resource.value = data.get('value')
        resource.resource_type = data['resource_type']
        db.session.commit()
        logging.info(f"Resource updated: {resource}")
        return resource_schema.jsonify(resource), 200
    except ValidationError as ve:
        logging.error(f"ValidationError: {ve.messages}")
        return jsonify({'error': 'Invalid data', 'messages': ve.messages}), 400
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        db.session.rollback()
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        logging.error(f"Exception: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

@bp.route('/resource/<name>', methods=['DELETE'])
def delete_resource(name):
    logging.info(f"DELETE /resource/{name}")
    try:
        resource = Resource.query.filter_by(name=name).first()
        if not resource:
            raise NotFound(f'Resource with name {name} does not exist')

        db.session.delete(resource)
        db.session.commit()
        logging.info(f"Resource deleted: {resource}")
        return jsonify({'message': f'Resource with name {name} deleted'}), 200
    except Exception as e:
        logging.error(f"Exception: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

@bp.route('/resource/search', methods=['GET'])
def search_resources():
    name = request.args.get('name')
    arn = request.args.get('arn')
    resource_type = request.args.get('resource_type')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Resource.query

    if name:
        query = query.filter(Resource.name.ilike(f"%{name}%"))
    if arn:
        query = query.filter(Resource.arn.ilike(f"%{arn}%"))
    if resource_type:
        query = query.filter(Resource.resource_type.ilike(f"%{resource_type}%"))

    resources_pagination = query.paginate(page, per_page, error_out=False)
    resources = resources_pagination.items
    total = resources_pagination.total

    response = {
        'total': total,
        'page': page,
        'per_page': per_page,
        'resources': resources_schema.dump(resources)
    }
    return jsonify(response), 200
