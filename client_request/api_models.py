import aiohttp


class AdvAPI:

    def __init__(self, host='http://localhost:8080'):
        self.host = host
        self.session = aiohttp.ClientSession()

    async def _call(self, http_method, api_method, response_type=None, *args, **kwargs):
        request_method = getattr(self.session, http_method)
        response = await request_method(f'{self.host}/{api_method}', *args, **kwargs)
        if response_type == 'json':
            response = await response.json()
        return response

    async def new_user(self, data):
        return await self._call('post', 'user', response_type='json', json=data)

    async def del_user(self, id):
        return await self._call('delete', f'user/{id}', response_type='json')

    async def get_user(self, character_id):
        return await self._call('get', f'user/{character_id}', response_type='json')

    async def update_user(self, character_id, data):
        return await self._call('patch', f'update/user/{character_id}', response_type='json', json=data)

    async def check_health(self):
        return await self._call('get', 'check_health', response_type='json')

    async def test_request(self):
        return await self._call('post', 'test', response_type='json', json={"key1": "value1"},
                                params={"key2": "value2"})

    async def new_adv(self, post_data_json):
        return await self._call('post', 'adv', response_type='json', json=post_data_json)

    async def del_adv(self, adv_id):
        return await self._call('delete', f'adv/{adv_id}', response_type='json')

    async def get_adv(self, adv_id):
        return await self._call('get', f'adv/{adv_id}', response_type='json')

    async def update_adv(self, adv_id, patch_data_json):
        return await self._call('patch', f'update/adv/{adv_id}', response_type='json', json=patch_data_json)

    async def close(self):
        await self.session.close()

# class CharacterGetFromURL:
#
#     def __init__(self, host='https://swapi.dev/api'):
#         self.host = host
#         self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
#
#     async def _call(self, http_method, api_method, response_type=None, *args, **kwargs):
#         request_method = getattr(self.session, http_method)
#         response = await request_method(f'{self.host}/{api_method}', *args, **kwargs)
#         if response_type == 'json':
#             response = await response.json()
#         return response
#
#     async def get_by_url(self, url):
#         return await self._call('get', url, response_type='json')
#
#     async def get_character(self, character_id):
#         return await self._call('get', f'people/{character_id}', response_type='json')
#
#     async def close(self):
#         await self.session.close()
#
#     async def get_full_data(self, id, template):
#         download_data = {}
#         response_json = await self.get_character(int(id))
#         if response_json == {'detail': 'Not found'}:
#             return
#
#         add_request_key = template.get('add_request_key')
#         download_data_key = template.get('outload_data_key')
#         key_to_name = template.get('key_to_name')
#
#         for key in add_request_key + download_data_key:
#             inner_request_data = response_json.get(key)
#             if key in download_data_key:
#                 key_value = inner_request_data if inner_request_data is not [] else ''
#                 download_data.setdefault(key, key_value)
#                 continue
#             if isinstance(inner_request_data, str) and inner_request_data != '':
#                 url_list = [inner_request_data]
#             else:
#                 url_list = inner_request_data
#             needed_key = key_to_name.get(key)
#             needed_value = ''
#
#             if url_list is not []:
#                 for url in url_list:
#                     add_url = url.replace(f'{self.host}/', '')
#                     ad_response = await self.get_by_url(add_url[:-1])
#                     needed_value += f'{ad_response.get(needed_key)}, '
#             download_data.setdefault(key, needed_value)
#
#         return download_data
