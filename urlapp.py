import falcon
import requests
from pymongo import MongoClient
import json
import uuid

# connection to mongo and db name here is urldb
db = MongoClient(host='0.0.0.0', port=27017).urldb



class JSONTranslator(object):
  """
    Json Parser for our app
  """
  def process_request(self, req, resp):
      if req.content_length in (None, 0) and req.method == 'GET':
          return
      body = req.stream.read()
      if not body:
          raise falcon.HTTPBadRequest('Empty request body',
                                      'A valid JSON document is required.')
      try:
          req.context['doc'] = json.loads(body.decode('utf-8'))
      except (ValueError, UnicodeDecodeError):
          raise falcon.HTTPError(falcon.HTTP_753,
                                 'Malformed JSON',
                                 'Could not decode the request body. The '
                                 'JSON was incorrect or not encoded as '
                                 'UTF-8.')

  def process_response(self, req, resp, resource):
      if 'result' not in req.context:
          resp.append_header('Access-Control-Allow-Origin', '*')
          resp.append_header('Access-Control-Allow-Methods', 'GET, POST')
          resp.append_header('Access-Control-Allow-Headers', 'Origin, Content-Type')
          return
      resp.append_header('Access-Control-Allow-Origin', '*')
      resp.append_header('Access-Control-Allow-Methods', 'GET, POST')
      resp.append_header('Access-Control-Allow-Headers', 'Origin, Content-Type')
      resp.body = json.dumps(req.context['result'])
      resp.append_header('Content-Type', 'application/json')


class Short:
  """
    This is an endpoint for url shortening
  """
  def on_post(self, req, resp):
    resp_dict = {"success": True, "summary": "Shortened url", "data": {}}
    try:
      doc = req.context["doc"]
      url = doc["url"]
      if "http" not in url:
        raise Exception("Not a valid url")
      r = requests.get(url)
      if r.status_code == 200:
        k = str(uuid.uuid4().hex[:8])
        s_url = "http://0.0.0.0:5000/"+ k
        db.urls.insert({"url": url, "sid": k, "myurl": s_url})
        resp_dict["data"] = {"shortened_url": s_url}
        resp.status_code = falcon.HTTP_201
      else:
        raise Exception("Not a valid url. Please give valid url")
    except Exception as e:
      resp_dict["summary"] = str(e)
      resp_dict["success"] = False
      resp.status_code = falcon.HTTP_502
    finally:
      req.context["result"] = resp_dict

class Gotoactualurl:
  """
    This is an endpoint for going to actual url from shorntend url
  """
  def on_get(self, req, resp, uid=None):
    resp_dict = {"success": True, "summary": "Redirected"}
    try:
      if not uid:
        raise Exception("Not a valid url")
      uobj = db.urls.find_one({"sid": uid})
      if uobj:
        resp.status = falcon.HTTP_302
        resp.set_header('Location',  uobj['url'])
      else:
        raise Exception("No such url exixts")
    except Exception as e:
      resp.status = falcon.HTTP_502
      resp_dict["summary"] = str(e)
      resp_dict["success"] = False
      req.context['result'] = resp_dict


# app creation 

app = falcon.API(middleware=[JSONTranslator()])

sobj = Short()
app.add_route('/shorten_url', sobj)

gobj = Gotoactualurl()
app.add_route('/{uid}', gobj)
