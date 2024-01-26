import asyncio
import random
import string
from datetime import datetime

import httpx


SERVER = 'http://127.0.0.1:8000/api'
EMAIL = 'some@email.com'
PASSWORD = 'SOMEpassword'


base_headers = {'Content-Type': 'application/json'}


async def create_user():
    print('Create user')
    data = {'email': EMAIL, 'password': PASSWORD, 'role': 1}
    async with httpx.AsyncClient() as client:
        r = await client.post(
            SERVER + '/authentication/user',
            headers=base_headers,
            json=data,
        )
        print(r)
        response = r.json()
        return response


async def login():
    print('Login')
    data = {'username': EMAIL, 'password': PASSWORD}
    async with httpx.AsyncClient() as client:
        r = await client.post(
            SERVER + '/authentication/user/login',
            data=data,
        )
        print(r)
        response = r.json()
        return response


def _generate_random_string(length=8):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def _generate_random_int_list(length=10):
    return [random.randint(-10, 10) for x in range(1, length)]


def generate_random_leads():
    leads = []
    random_name = _generate_random_string()
    negative_count = 0
    for n in range(1, 20):
        lead = {
            'id': f'{random_name}{n}',
            'name': random_name,
            'signal': _generate_random_int_list(),
        }
        negative_count += len(list(filter(lambda x: (x < 0), lead['signal'])))
        leads.append(lead)
    return leads, negative_count


async def create_ecg(token):
    print('Create ecg')
    headers = {'Authorization': f'Bearer {token}'}
    headers.update(base_headers)
    leads, negative_count = generate_random_leads()
    data = {
        'date': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        'leads': leads,
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(
            SERVER + '/ecg',
            headers=headers,
            json=data,
        )
        print(r)
        response = r.json()
        return response['id'], negative_count


async def get_insights(token):
    print('Get ecg with insights')
    headers = {'Authorization': f'Bearer {token}'}
    headers.update(base_headers)
    async with httpx.AsyncClient() as client:
        r = await client.get(
            SERVER + '/insights',
            headers=headers,
        )
        print(r)
        response = r.json()
        return response


async def main():
    await create_user()
    response = await login()
    token = response['access_token']
    tasks = []
    inserts = random.randint(1, 15)
    for _ in range(0, inserts):
        tasks.append(asyncio.create_task(create_ecg(token)))
    results = await asyncio.gather(*tasks)

    print(f'{inserts} ecgs inserted properly.')

    data_to_check = {}
    for r in results:
        data_to_check[r[0]] = r[1]

    print('Sleeping 3 sec (waiting for the background tasks)...')
    await asyncio.sleep(3.)

    insights = await get_insights(token)
    
    print(f'Checking insights correctness: {data_to_check}')
    for insight in insights:
        expected_negative_count = data_to_check.get(insight['id'], 0)
        equal = expected_negative_count == insight['negative_count']
        print(f"Comparing {expected_negative_count} with {insight['negative_count']} = {equal}")

    print('Test finish')


asyncio.run(main())
