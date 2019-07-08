# from sqlalchemy.orm import Session
# from app.models.models import User, UserAnswer, UserCache
#
#
# class userDAO:
#
#     def create_user(self, vk_id, first_name, last_name, menu_name):
#         user = User.create(vk_id, first_name, last_name).create_cache(menu_name)
#         return user
#
#     def user_inc_request(self, vk_id):
#         user = User.get_user(vk_id).inc_request()
#         return user
#
#     def add_answer(self, vk_id, answer):
#         user = User.get_user(vk_id).add_answer(answer)
#         return user
#
#     def clear_answers(self, vk_id):
#         user = User.get_user(vk_id).clear_answers()
#         return user
#
#     def update_user(self, vk_id, **kwargs):
#         user = User.get_user(vk_id)
#         if kwargs.get('special_answers'):
#             user.add_answer(kwargs.get('special_answers'))
#         elif type(kwargs.get('special_answers'))==list:
#             user.clear_answers()
#
#         user.update(first_name=kwargs.get('first_name'),
#                     last_name=kwargs.get('last_name'),
#                     total_requests=kwargs.get('total_requests'),
#                     user_cache=kwargs.get('user_cache'),
#                     answers=kwargs.get('special_answers'))
#         return user
