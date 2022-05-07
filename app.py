from aiohttp import web
import config


from models import db
from views import AdvView, UserView

app = web.Application()


async def check_health(request):
    return web.json_response({'status': 'OK'})


async def test_request(request: web.Request):
    json_data = await request.json()
    return web.json_response({
        'headers': dict(request.headers),
        'json': json_data,
        'qs': dict(request.query),
    })


app.add_routes([
    web.get('/check_health', check_health),
    web.get('/user/{id:\d+}', UserView),
    web.post('/user', UserView),
    web.delete('/user/{id:\d+}', UserView),
    web.patch('/update/user/{id:\d+}', UserView),
    web.get('/adv/{id:\d+}',AdvView),
    web.delete('/adv/{id:\d+}',AdvView),
    web.patch('/update/adv/{id:\d+}',AdvView),
    web.post('/adv', AdvView)
])


async def init_orm(app):
    await db.set_bind(config.PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


app.cleanup_ctx.append(init_orm)
web.run_app(app)


async def get_app():
    return app
