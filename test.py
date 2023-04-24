from requests import *

from requests import get, post, delete

# {'error': 'Id already exists.'} id=2 уже существует
print(put('http://127.0.0.1:8080/api/jobs/2',
           json={'team_leader': 1,
                 'title': 'Текст новости',
                 'job': 'cddfvdds',
                 'work_size': 12,
                 'collaborators': '1, 2, 3',
                 'is_finished': False}).json())





