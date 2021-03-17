var selectedServer = 'JS';
var selectedCase = 'case1';
var firstUsers = '1';

const servers = [
  {
    type: 'JS',
    name: 'JavaScript',
    url: 'http://localhost:4000/'
  },
  {
    type: 'PYTHON',
    name: 'Python',
    url: 'http://localhost:8000/graphql_server'
  },
  {
    type: 'GO',
    name: 'Go',
    url: 'http://localhost:8080/query'
  },
];

const cases = [
  {
    id: 'case1',
    name: 'Caso 1',
    query: (first) => `
      query {
        users (first: ${first}) {
          id
          name
          last_name
          email
          address
          birthday
        }
      }
    `
  },
  {
    id: 'case2',
    name: 'Caso 2',
    query: (first) => `
      query {
        users (first: ${first}) {
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
    `
  },
  {
    id: 'case3',
    name: 'Caso 3',
    query: (first) => `
      query {
        users (first: ${first}) {
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
    `
  }
];

const tests = [];

function onFirstUsersChange() {
  const input = document.getElementById('firstUsers');
  input.addEventListener('input', function (e) {
    firstUsers = input.value.trim();
    input.value = firstUsers;

    if (!firstUsers || isNaN(+firstUsers) || +firstUsers <= 0) {
      document.getElementById('submitButton').setAttribute('disabled', true);
    } else {
      document.getElementById('submitButton').removeAttribute('disabled');
    }
  });
}

function setServer() {
  const select = document.getElementById('serverSelect');
  selectedServer = select.options[select.selectedIndex].value;
}

function setCase() {
  const caseSelect = document.getElementById('caseSelect');
  selectedCase = caseSelect.options[caseSelect.selectedIndex].value;
}

function createRowCell(text, className) {
  const cell = document.createElement('div');
  cell.className = className;
  const secondstitle = document.createTextNode(text);
  cell.appendChild(secondstitle);

  return cell;
}
async function query() {
  console.log(`Getting info for case ${selectedCase}, server ${selectedServer}, and firstUsers ${firstUsers}...`,);

  const server = servers.find(function (s) { return s.type === selectedServer });
  const url = server.url;

  const currentCase = cases.find(function (c) { return c.id === selectedCase });
  const queryString = currentCase.query(firstUsers);

  const btn = document.getElementById('submitButton');
  const list = document.getElementById('testsList');
  btn.setAttribute('disabled', true);
  const headers = {
    'Content-Type': 'application/json',
  };

  if (server.type === 'GO') {
    headers['X-FirstUsers'] = firstUsers; // Header for Go server
  }

  const startTime = new Date().getTime();
  try {
    const response = await fetch(url, {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'X-FirstUsers': firstUsers, // Header for Go server
      },
      body: JSON.stringify({
        query: queryString
      })
    });
    const seconds = (new Date().getTime() - startTime) / 1000;

    const data = await response.json();

    if (data.errors && data.errors.length > 0) {
      alert(`Errors! ${data.errors.join(', ')}`)
    } else {
      const newRow = document.createElement('div');
      newRow.className = 'row';

      const serverCell = createRowCell(server.name, 'server');
      const caseCell = createRowCell(currentCase.name, 'case');
      const firstUsersCell = createRowCell(firstUsers, 'first');
      const timeCell = createRowCell(seconds, 'time');

      newRow.appendChild(serverCell);
      newRow.appendChild(caseCell);
      newRow.appendChild(firstUsersCell);
      newRow.appendChild(timeCell);

      tests.unshift({
        id: new Date().getTime(),
        firstUsers,
        time: seconds,
        serverType: server.type,
        serverName: server.name,
        caseId: currentCase.id,
        caseName: currentCase.name,
      });

      list.prepend(newRow);
    }
  } catch (error) {
    console.error('Error getting data!', error);
    alert('Error!!! ' + error.message);
  } finally {
    btn.removeAttribute('disabled');
  }
}

onFirstUsersChange();