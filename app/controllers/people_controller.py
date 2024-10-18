from flask import Blueprint, jsonify, request
import json
import os
from loguru import logger
from use_cases.get_people import GetPeopleUseCase
from repositories.people_repository import PeopleRepository

people = Blueprint("people", __name__)

def serialize_data(data):
    return data.__dict__

@people.route('/', methods=['GET'])
def get_status():
    return jsonify({"message": "Flask app up and running"})

@people.route('/data', methods=['GET'])
def get_sorted_people():
    # Get URL params: page and all
    page = request.args.get('page', default=None, type=int)
    get_all = request.args.get('all', default="false").lower() == "true"

    logger.info("Received request to fetch results")

    # Repository and use case setup
    api_url = os.getenv("API_URL")
    people_repository = PeopleRepository(api_url, logger)
    get_people_use_case = GetPeopleUseCase(people_repository, logger)

    try:
        if get_all:
            # Get all pages if 'all=true' is as URL param (it has priority over 'page')
            sorted_people = get_people_use_case.execute()
        elif page:
            # Get an specific page if 'page' is as URL param
            sorted_people = get_people_use_case.execute(page=page)
        else:
            # If any of the params is specified, by default we will get the first page
            sorted_people = get_people_use_case.execute(page=1)

        # Serialize to JSON
        result = [serialize_data(p) for p in sorted_people]

        logger.info("Returning results...")

        return jsonify(result)
    except Exception as e:
        logger.error(f"An error ocurred: {e}")
        return jsonify({"error": str(e)}), 400
