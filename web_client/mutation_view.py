from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from web_client.models import TestMutation
from .forms import TestMutationForm
import time
from datetime import datetime, timezone
import pytz
from promise import Promise
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from graphql import build_ast_schema, parse
from .commons import servers, pythonServerType

with open('web_client/schema.graphql') as source:
    document = parse(source.read())

schema = build_ast_schema(document)

tests = []

clientsTotal = 1

serverType = pythonServerType

querying = False

async def performMutation(serverType, clientsTotal):
  global querying
  print("Running mutation...", serverType, clientsTotal)
  if querying == True:
    print("Not going to run mutation. Already running a mutation")
    return;

  querying = True
  headers = {
    "Content-type": "application/json",
  }
  if serverType == 'GO':
    headers['X-clientsTotal'] = f'{clientsTotal}'

  print("Creating client againts server", serverType, servers[serverType]['url'])
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
  
  createdAt = datetime.now(timezone.utc).isoformat()
  
  for i in range(clientsTotal):
    index = i + 1
    try:
      query = gql('''
        mutation CreateClient($client: ClientInput!){
          createClient(client: $client) {
            id
            name
          }
        }
      ''')
      r = client.execute(query, variable_values={"client": {
        "name": f'Juan {index} PYTHON',
        "email": f'jp{index}@mail.com',
        "last_name": f'P\u00E9rez {index}',
        "birthday": datetime(1990, (i % 12) + 1, (i % 28) + 1, 10, 0, 0, 0, pytz.UTC).isoformat() ,
        "address": f'Avenida de las Merceditas y Calle XYZ-{index}',
        "created_at": createdAt
      }})
      # print("RESPONSE", r)

    except Exception as e:
      print('Error creating client...', i, e)
      querying = False    
      return

  newTest = TestMutation(
    id = time.time(),
    clientsTotal = clientsTotal,
    serverType = serverType,
    serverName = servers[serverType]['name'],
    time = '{0:.3f}'.format(time.time() - startTime)
  )

  tests.insert(0, newTest)
  
  print("END TIME", newTest.time)

  querying = False


async def index(request):
  formValid = True;
  global querying
  global clientsTotal
  global serverType

  showQueryingMessage = querying == True

  if request.method == 'POST':
      # create a form instance and populate it with data from the request:
      form = TestMutationForm(request.POST)
      formValid = form.is_valid()
      if form.is_valid():
        clientsTotal = form.cleaned_data['clientsTotal'];
        serverType = form.cleaned_data['serverType'];

        if (querying == False):
          await performMutation(serverType, clientsTotal)

          # redirect to a new URL to avoid the problem of resubmitting the form when the page is refreshed:
        return HttpResponseRedirect('/python_web_client/mutation/')
      else:
        formValid = False
  # if a GET (or any other method) we'll create a blank form
  else:
    form = TestMutationForm(initial={
      'clientsTotal': clientsTotal,
      'serverType': serverType,
    })

  template = loader.get_template('web_client/mutation.html')

  context = {
    'tests': tests,
    'form': form,
    'formValid': formValid,
    'showQueryingMessage': showQueryingMessage
  }
  return HttpResponse(template.render(context, request))
