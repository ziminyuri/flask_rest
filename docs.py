from app import docs
from views import (add_comment, add_post, delete_comment, delete_post,
                   get_comments, get_posts, registration, update_comment,
                   update_post, get_users)

docs.register(registration)
docs.register(get_posts)
docs.register(add_post)
docs.register(update_post)
docs.register(delete_post)
docs.register(get_comments)
docs.register(add_comment)
docs.register(update_comment)
docs.register(delete_comment)
docs.register(get_users)