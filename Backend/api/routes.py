from flask import Blueprint, request, jsonify
from .models import Resource
from .schema import ResourceSchema
from . import db
import logging
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

bp = Blueprint('api', __name__, url_prefix='/api')
logging.basicConfig(level=logging.INFO)

resource_schema = ResourceSchema()
resources_schema = ResourceSchema(many=True)

@bp.route('/namespace', methods=['POST'])
def create_namespace():
    data = request.get_json()
    namespace = data.get('namespace')
    if not namespace:
        return jsonify({'error': 'Namespace is required'}), 400

    # Check if namespace already exists
    existing_namespace = db.session.query(Resource.namespace.distinct()).filter_by(namespace=namespace).first()
    if existing_namespace:
        return jsonify({'error': 'Namespace already exists'}), 409

    # Create a dummy resource to register the namespace
    dummy_resource = Resource(name=f'{namespace}_dummy', arn='', namespace=namespace, resource_type='dummy')
    db.session.add(dummy_resource)
    db.session.commit()
    db.session.delete(dummy_resource)
    db.session.commit()

    return jsonify({'message': 'Namespace created'}), 201

@bp.route('/resource/<namespace>', methods=['POST'])
def add_resource(namespace):
    data = request.get_json()
    logging.info(f"POST /resource/{namespace} data: {data}")

    try:
        resource_schema.load(data)
        if Resource.query.filter_by(name=data['name'], namespace=namespace).first():
            logging.info("Resource with this name already exists in this namespace")
            return jsonify({'error': 'Resource with this name already exists'}), 409

        resource = Resource(**data, namespace=namespace)
        db.session.add(resource)
        db.session.commit()
        logging.info(f"Resource created: {resource}")

        return resource_schema.dump(resource), 201
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

@bp.route('/resource/<namespace>/<name>', methods=['GET'])
def get_resource(namespace, name):
    logging.info(f"GET /resource/{namespace}/{name}")
    resource = Resource.query.filter_by(name=name, namespace=namespace).first_or_404()
    logging.info(f"Resource found: {resource}")
    return resource_schema.dump(resource), 200

@bp.route('/resource/<namespace>/all', methods=['GET'])
def get_all_resources(namespace):
    try:
        logging.info(f"GET /resource/{namespace}/all")
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        resources_pagination = Resource.query.filter_by(namespace=namespace).paginate(page=page, per_page=per_page, error_out=False)
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
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

@bp.route('/resource/<namespace>/<name>', methods=['PUT'])
def update_resource(namespace, name):
    data = request.get_json()
    logging.info(f"PUT /resource/{namespace}/{name} data: {data}")

    try:
        resource_schema.load(data)
        resource = Resource.query.filter_by(name=name, namespace=namespace).first()
        if not resource:
            raise NotFound(f'Resource with name {name} does not exist in namespace {namespace}')

        resource.arn = data.get('arn')
        resource.value = data.get('value')
        resource.resource_type = data.get('resource_type')
        db.session.commit()
        logging.info(f"Resource updated: {resource}")
        return resource_schema.dump(resource), 200
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

@bp.route('/resource/<namespace>/<name>', methods=['DELETE'])
def delete_resource(namespace, name):
    logging.info(f"DELETE /resource/{namespace}/{name}")
    try:
        resource = Resource.query.filter_by(name=name, namespace=namespace).first()
        if not resource:
            raise NotFound(f'Resource with name {name} does not exist in namespace {namespace}')

        db.session.delete(resource)
        db.session.commit()
        logging.info(f"Resource deleted: {resource}")
        return jsonify({'message': f'Resource with name {name} deleted'}), 200
    except Exception as e:
        logging.error(f"Exception: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

@bp.route('/resource/<namespace>/search', methods=['GET'])
def search_resources(namespace):
    name = request.args.get('name')
    arn = request.args.get('arn')
    resource_type = request.args.get('resource_type')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Resource.query.filter_by(namespace=namespace)

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

@bp.route('/namespaces', methods=['GET'])
def get_all_namespaces():
    try:
        logging.info("GET /namespaces")
        namespaces = db.session.query(Resource.namespace.distinct()).all()
        namespace_list = [ns[0] for ns in namespaces]

        logging.info(f"Namespace list: {namespace_list}")
        return jsonify({'namespaces': namespace_list}), 200
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

@bp.route('/resources', methods=['GET'])
def get_all_resources_all_namespaces():
    try:
        logging.info("GET /resources")
        resources = Resource.query.all()
        logging.info(f"Resources list: {resources}")
        response = resources_schema.dump(resources)
        return jsonify(response), 200
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500
