from graphql_server.middlewares import Loaders
from django.shortcuts import render
import json
from django.http import JsonResponse
from graphql_server.schema import schema

def index(request):  
  body = json.loads(request.body.decode('utf-8'))
  
  variables = {}
  if 'variables' in body:
    variables = body['variables']
  result = schema.execute(body['query'], variables = variables, context={ 'loaders': Loaders() })
    
  response = { 'data': result.data }

  # As result.errors is not serializable, then create errors array manually
  errors = [{'message': ob.message } for ob in (result.errors or [])]
  if (len(errors) > 0) :
    response['errors'] = errors;
  
  return JsonResponse(response)