# from apps.blog_home_work.models import Posts
# from datetime import datetime, timezone
#
# def get_title(value):
#     title = value
#     post = Posts.objects.all()
#     for title in post:
#         time_post = title.date_publication
#         if title.title == title:
#             time_now = datetime.now(timezone.utc)
#             d = time_now - time_post
#             q = d.days
#             if q >= 1:
#                 #резрешить публикацию
#             else:
#                 #невозможно создать пост с одинаковыми заголовками в течении 1-х суток
