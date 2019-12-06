import os
from flask_restful import Api
from datA import app, api
from datA.datalist import RegisterUser, LoginUser, Datalist, DatalistItem, SingleDatalist, SingleDatalistItem


api.add_resource(RegisterUser, '/auth/register/')
api.add_resource(LoginUser, '/auth/login/')
api.add_resource(Datalist, '/datalists/')
api.add_resource(SingleDatalist, '/datalists/<int:ID>')
api.add_resource(DatalistItem, '/datalists/<int:ID>/items/')
api.add_resource(SingleDatalistItem, '/datalists/<int:ID_data>/items/<int:ID_item>')

if __name__ == '__main__':
    api = Api(app=app)
    app.run(host='0.0.0.0')
