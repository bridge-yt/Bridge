from flask import Blueprint, request, jsonify
from .models import Resource
from . import db
import logging
from sqlalchemy.exc import IntegrityError

bp = Blueprint('api', __name__, url_prefix='/api')

logging.basicConfig(level=logging.DEBUG)

@bp.route('/resource', methods=['POST'])
def add_resource():
    data = request.json
    logging.debug(f"POST /resource data: {data}")
    try:
        if Resource.query.filter_by(name=data['name']).first():
            logging.debug("Resource with this name already exists")
            return jsonify({'status': 'error', 'message': 'Resource with this name already exists'}), 400
        resource = Resource(
            name=data['name'],
            arn=data['arn'],
            value=data.get('value'),  # Use .get to allow None
            resource_type=data['resource_type']
        )
        db.session.add(resource)
        db.session.commit()
        logging.debug(f"Resource created: {resource}")
        return jsonify({
            'name': resource.name,
            'arn': resource.arn,
            'value': resource.value,
            'resource_type': resource.resource_type,
            'created_at': resource.created_at
        }), 201  # Return 201 Created status
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Database Integrity Error: ' + str(e)}), 500
    except Exception as e:
        logging.error(f"Exception: {e}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Internal Server Error: ' + str(e)}), 500

@bp.route('/resource/<name>', methods=['GET'])
def get_resource(name):
    logging.debug(f"GET /resource/{name}")
    resource = Resource.query.filter_by(name=name).first_or_404()
    logging.debug(f"Resource found: {resource}")
    return jsonify({
        'name': resource.name,
        'arn': resource.arn,
        'value': resource.value,
        'resource_type': resource.resource_type,
        'created_at': resource.created_at,
        'updated_at': resource.updated_at
    }), 200

@bp.route('/resource/all', methods=['GET'])
def get_all_resources():
    logging.debug("GET /resource/all")
    resources = Resource.query.all()
    resources_list = [{
        'name': r.name,
        'arn': r.arn,
        'value': r.value,
        'resource_type': r.resource_type,
        'created_at': r.created_at,
        'updated_at': r.updated_at
    } for r in resources]
    logging.debug(f"Resources list: {resources_list}")
    return jsonify(resources_list), 200

@bp.route('/resource/<name>', methods=['PUT'])
def update_resource(name):
    data = request.json
    logging.debug(f"PUT /resource/{name} data: {data}")
    try:
        resource = Resource.query.filter_by(name=name).first()
        if not resource:
            logging.debug(f"Resource with name {name} does not exist")
            return jsonify({'status': 'error', 'message': f'Resource with name {name} does not exist'}), 404

        resource.arn = data['arn']
        resource.value = data.get('value')  # Use .get to allow None
        resource.resource_type = data['resource_type']
        db.session.commit()
        logging.debug(f"Resource updated: {resource}")
        return jsonify({
            'name': resource.name,
            'arn': resource.arn,
            'value': resource.value,
            'resource_type': resource.resource_type,
            'updated_at': resource.updated_at
        }), 200  # Return 200 OK status
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Database Integrity Error: ' + str(e)}), 500
    except Exception as e:
        logging.error(f"Exception: {e}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Internal Server Error: ' + str(e)}), 500

@bp.route('/resource/<name>', methods=['DELETE'])
def delete_resource(name):
    logging.debug(f"DELETE /resource/{name}")
    try:
        resource = Resource.query.filter_by(name=name).first()
        if not resource:
            logging.debug(f"Resource with name {name} does not exist")
            return jsonify({'status': 'error', 'message': f'Resource with name {name} does not exist'}), 404
        db.session.delete(resource)
        db.session.commit()
        logging.debug(f"Resource deleted: {resource}")
        return jsonify({'status': 'success', 'message': f'Resource with name {name} deleted'}), 200  # Return 200 OK status
    except Exception as e:
        logging.error(f"Exception: {e}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Internal Server Error: ' + str(e)}), 500
