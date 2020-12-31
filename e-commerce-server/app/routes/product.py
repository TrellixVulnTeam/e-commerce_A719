from flask_restful import Resource, reqparse, marshal_with , fields
from flask_jwt_extended import jwt_required

from app.db.category import *
from app.db.product import *
from app import api

product_fields = {
    'id': fields.String(attribute=lambda x: x.id),
    'name': fields.String(attribute=lambda x: x.name),
    'price': fields.String(attribute=lambda x: x.price),
    'quantity': fields.String(attribute=lambda x: x.quantity),
    'category_name': fields.String(attribute=lambda x: x.category.name),
    'category_id': fields.String(attribute=lambda x: x.category.id)
}

product_filter_parser = reqparse.RequestParser()
product_filter_parser.add_argument('name', type=str, required=False)

class ProductsResource(Resource):
    @marshal_with(product_fields)
    def get(self):
        products = product_filter_parser.parse_args()
        query = Product.query.outerjoin(Category)
        if 'name' in products:
            query.filter_by(Product.name.contains(products['name']))
        return query


product_parser = reqparse.RequestParser()
product_parser.add_argument('quantity', type=int)

class ProductResource(Resource):
    @jwt_required
    def post(self, id):
        quantity = product_parser.parse_args()['quantity']
        query = Product.get(id).first()
        if query and query.qunatity >= quantity:
            query.quantity -= quantity
            return {'message': 'added successfully'}

        return {'message': 'something went wrong'}

api.add_resource(ProductsResource, '/products')
api.add_resource(ProductResource, '/product/<int:id>')