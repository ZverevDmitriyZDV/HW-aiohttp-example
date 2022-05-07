from aiohttp import web
from asyncpg import UniqueViolationError
from models import User, UserValidationModel, Adv, AdvValidationModel, db
from pydantic import BaseModel
from utils import hash_password_in_dict, patch_json_data


class TemplateView(web.View):
    model_class: db.Model
    class_valid: BaseModel

    async def delete(self):
        id = int(self.request.match_info['id'])
        element = await self.model_class.get(id)
        if element is None:
            return web.json_response({"error": "not found for delete"}, status=404)
        await element.delete()
        return web.json_response({"deleted": "ok"}, status=200)

    async def get(self):
        id = int(self.request.match_info['id'])
        element = await self.model_class.get(id)
        if element is None:
            return web.json_response({"error": "not found"}, status=404)
        data = element.to_dict()
        return web.json_response(data)

    async def post(self):
        json_data = await self.request.json()
        json_data_validated = self.class_valid(**hash_password_in_dict(json_data)).dict()
        print(json_data_validated)
        try:
            new_elem = await self.model_class.create(**json_data_validated)
        except UniqueViolationError:
            return web.json_response({'error': 'Already exist'}, status=400)
        return web.json_response(new_elem.to_dict())

    async def patch(self):
        id = int(self.request.match_info['id'])
        elem = await self.model_class.get(id)
        if elem is None:
            return web.json_response({"error": "not found for update"}, status=404)
        json_get_data = elem.to_dict()
        json_data = hash_password_in_dict(await self.request.json())
        patch_data = patch_json_data(json_get_data, json_data)
        await elem.update(**patch_data).apply()
        elem_after = await self.model_class.get(id)
        if json_get_data != elem_after.to_dict():
            return web.json_response({"status": 'Udated',
                                      'after': elem_after.to_dict()}, status=200)
        return web.json_response({"error": "not updated"}, status=404)


class AdvView(TemplateView):
    model_class = Adv
    class_valid = AdvValidationModel


class UserView(TemplateView):
    model_class = User
    class_valid = UserValidationModel
