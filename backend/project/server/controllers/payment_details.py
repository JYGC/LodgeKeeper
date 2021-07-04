'''
All API endpoints that handle payment detail models and actions
'''

import traceback
from flask.views import MethodView
from flask import Blueprint, request, jsonify, session

from project.server import db, app
from project.server.models.user import User
from project.server.models.payment_details import PaymentDetailsFetcher

class GetAllPaymentDetails(MethodView):
    ''' Get all payment details of the account '''
    def post(self):
        ''' POST request '''
        try:
            pd_fetcher = PaymentDetailsFetcher(db.session, db.session.query(
                User.account_id
            ).filter(User.id == int(session.pop('user_id', None))).first()[0])

            payment_details = pd_fetcher.payment_details_to_dict()
        except Exception as ex:
            pass