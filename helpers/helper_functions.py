from instauser.models import InstaUser
from post.models import Post



def get_tags(text):
    tags = []
    for word in text.split():
        if word.startswith('@') != 0:
            tag = word[1:]
            user = InstaUser.objects.get(username=tag)
            tags.append(tag)
    return tags