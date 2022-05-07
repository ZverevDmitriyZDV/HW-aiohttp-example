import asyncio

from client_request.api_models import AdvAPI


async def main():
    connection = AdvAPI()
    # print(await connection.del_user(100))
    print(await connection.get_user(1))
    new_user = {
        'user_name': 'u1',
        'user_password': 'p1',
        'user_email': 'u1@masd.su'
    }
    print(await connection.new_user(new_user))
    new_data = {
        'user_name': '112'
    }
    print(await connection.update_user(1, new_data))
    new_user2 = {
        'user_name': 'u2',
        'user_password': 'p2',
        'user_email': 'u1@masd.su'
    }
    # print(await connection.del_user(1))

    print(await connection.get_adv(1))
    new_adv = {
        'header': 'h1',
        'description': 'best_day_in_hell for you',
        'owner': 1
    }
    print(await connection.new_adv(new_adv))

    update_adv = {
        'header': 'h1-1'
    }
    print(await connection.update_adv(1, update_adv))
    print(await connection.del_adv(1))

    await connection.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
