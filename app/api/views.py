"""API views for FM and LM table lookups."""

from http import HTTPStatus

from flask import Blueprint, request
from flask_restx import Api, Resource, reqparse

from app.api.services import lookup, validate_input

api_bp = Blueprint("api", __name__)

api = Api(
    api_bp,
    title="Infobip Logistics API",
    description="API for CEP + vehicle type lookups on FM and LM tables",
)

query_parser = reqparse.RequestParser()
query_parser.add_argument("cep", type=str, required=True, help="CEP (8 digits)")
query_parser.add_argument(
    "vehicle_type", type=str, required=False, help="Vehicle type (e.g. VUC, HR, VAN)"
)


@api.route("/validate")
class ValidateResource(Resource):
    """Validate CEP + vehicle type combination."""

    @api.expect(query_parser)
    def get(self):
        """Validate if CEP and vehicle_type are accepted."""
        args = query_parser.parse_args()
        cep = args["cep"]
        vehicle_type = args.get("vehicle_type", "")

        if not vehicle_type:
            return {"valid": False, "errors": ["vehicle_type is required"]}, HTTPStatus.BAD_REQUEST

        result = validate_input(cep, vehicle_type, table="fm")
        if not result["valid"]:
            return result, HTTPStatus.BAD_REQUEST
        return result, HTTPStatus.OK


@api.route("/fm")
class FMResource(Resource):
    """Query FM (First Mile) table."""

    @api.expect(query_parser)
    def get(self):
        """Look up FM table by CEP and optional vehicle type."""
        args = query_parser.parse_args()
        cep = args["cep"]
        vehicle_type = args.get("vehicle_type")

        rows = lookup(cep, vehicle_type, table="fm")
        if not rows:
            return {"message": "No results found", "cep": cep, "vehicle_type": vehicle_type}, HTTPStatus.NOT_FOUND

        return {"count": len(rows), "results": rows}, HTTPStatus.OK


@api.route("/lm")
class LMResource(Resource):
    """Query LM (Last Mile) table."""

    @api.expect(query_parser)
    def get(self):
        """Look up LM table by CEP and optional vehicle type."""
        args = query_parser.parse_args()
        cep = args["cep"]
        vehicle_type = args.get("vehicle_type")

        rows = lookup(cep, vehicle_type, table="lm")
        if not rows:
            return {"message": "No results found", "cep": cep, "vehicle_type": vehicle_type}, HTTPStatus.NOT_FOUND

        return {"count": len(rows), "results": rows}, HTTPStatus.OK
