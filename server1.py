from __future__ import print_function
import sys
import urllib
import urllib2
from sqlalchemy import create_engine

from flask import Flask
from flask_restplus import Api, Resource
from flask_jsonpify import jsonify
from flask import request


db_connect = create_engine('sqlite:///monitor.db')
app = Flask(__name__)
api = Api(app=app)
# install ()alternative handler to stop urllib2 from following redirects


# class NoRedirectHandler(urllib2.HTTPRedirectHandler):
#     # alternative handler
#     def http_error_401(self, req, fp, code, msg, header_list):
#         data = urllib.addinfourl(fp, header_list, req.get_full_url())
#         data.status = code
#         data.code = code

#         return data
class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_401 = http_error_302
    # http_error_301 = http_error_302
    # http_error_303 = http_error_302
    # http_error_307 = http_error_302


opener = urllib2.build_opener(NoRedirectHandler())
urllib2.install_opener(opener)


@api.route("/sites/")
class Sites(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        # This line performs query and returns json result
        query = conn.execute("select name from sites")
        result = [i[0] for i in query.cursor.fetchall()]
        content = []
        for r in result:
            try:
                status = urllib2.urlopen(r).getcode()
                x = {
                    "name": r,
                    "status": status
                }
                content.append(x)
            except Exception as e:
                print('Error', e, r, file=sys.stderr)

        content = jsonify(content)
        conn.close()
        return content

    @api.response(204, 'Category successfully created.')
    def post(self):
        conn = db_connect.connect()
        # all_cols = cursor.fetchall()
        # data = request.get_json()
        site_name = request.get_json()
        conn.execute("INSERT INTO site(name) VALUES (?)", (site_name['url']))
        conn.close()
        # print("{site_name}".format(site_name=site_name))
        print(site_name['url'])
        return None, 204

    @api.response(204, 'Category successfully updated.')
    def put(self):
        # all_cols = cursor.fetchall()
        data = request.get_json()
        print("{data}".format(data=data))
        return None, 204

    @api.response(204, 'Category successfully deleted.')
    def delete(self):
        # all_cols = cursor.fetchall()
        data = request.get_json()
        print("{data}".format(data=data))
        return None, 204


# @api.route("/conferences/<int:id>")
# class Conference(Resource):
#     def get(self, id):
#         """
#         Displays a conference's details
#         """

#     def put(self, id):
#         """
#         Edits a selected conference
#         """

app.run(port='5002', debug=True)
