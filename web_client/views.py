from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from web_client.models import Test
from .forms import TestForm
import time
from promise import Promise
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from graphql import build_ast_schema, parse
from .commons import servers, pythonServerType

with open('web_client/schema.graphql') as source:
    document = parse(source.read())

schema = build_ast_schema(document)

tests = []

firstUsers = 1
serverType = pythonServerType
caseId = 'case1'

cases = {
  'case1': {
    'name': 'Caso 1',
    'query': '''
       query Users($first: Int!) {
        users (first: $first) {
           id
          name
          last_name
          email
          address
          birthday
        } 
      }
    '''    
  },
  'case2': {
    'name': 'Caso 2',
    'query': '''
       query Users($first: Int!) {
        users (first: $first) {
           id
          name
          last_name
          email
          address
          birthday
          posts {
            title
            description
          }
        } 
      }
    '''
  },
  'case3': {
    'name': 'Caso 3',
    'query': '''
      query Users($first: Int!) {
        users (first: $first) {
           id
          name
          last_name
          email
          address
          birthday
          posts {
            title
            description
            comments {
              post_id
              description
            }
          }
        } 
      }
    '''
  }
}

querying = False

async def performQuery(caseId, serverType, firstUsers):  
  global querying
  
  if querying == True:
    print("Not going to run the query. Already running one...")
    return;

  querying = True

  print("QUERYING...", caseId, serverType, firstUsers)
  headers = {
    "Content-type": "application/json",
  }
  if serverType == 'GO':
    headers['X-FirstUsers'] = f'{firstUsers}'
  startTime = time.time()
  sample_transport=RequestsHTTPTransport(
    url=servers[serverType]['url'],
    use_json=True,
    headers=headers,
    verify=False,
    retries=1,
  )

  client = Client(
    transport=sample_transport,
    schema=schema,
  )
  
  try:
    query = gql(cases[caseId]['query'])
    r = client.execute(query, variable_values={"first": firstUsers}) 
    # test.time = '{0:.3f}'.format(time.time() - startTime)
    # # print("RESPONSE", r)
    

    newTest = Test(
      id = time.time(),
      firstUsers = firstUsers,
      time = '{0:.3f}'.format(time.time() - startTime),
      serverType = serverType,
      serverName = servers[serverType]['name'],
      caseId = caseId,
      caseName = cases[caseId]['name'],
    )
    tests.insert(0, newTest)

    print("END TIME", newTest.time)

    querying = False
  except Exception as e:
    print('Error querying...', e)
    querying = False


async def index(request):
  formValid = True;
  global querying
  global firstUsers
  global serverType
  global caseId

  showQueryingMessage = querying == True

  if request.method == 'POST':
      # create a form instance and populate it with data from the request:
      form = TestForm(request.POST)
      formValid = form.is_valid()
      if form.is_valid():
        firstUsers = form.cleaned_data['firstUsers'];
        serverType = form.cleaned_data['serverType'];
        caseId = form.cleaned_data['caseId'];        

        # if (querying == False):
        await performQuery(caseId, serverType, firstUsers)

          # redirect to a new URL to avoid the problem of resubmitting the form when the page is refreshed:
        return HttpResponseRedirect('/python_web_client/')
      else:
        formValid = False
  # if a GET (or any other method) we'll create a blank form
  else:
    form = TestForm(initial={
      'firstUsers': firstUsers,
      'serverType': serverType,
      'caseId': caseId,
    })

  template = loader.get_template('web_client/index.html')

  context = {
    'tests': tests,
    'form': form,
    'formValid': formValid,
    'showQueryingMessage': showQueryingMessage
  }
  return HttpResponse(template.render(context, request))
