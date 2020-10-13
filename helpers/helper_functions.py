from instauser.models import InstaUser
from post.models import Post



def get_tags(text):
    tags = []
    for word in text.split():
        if word.startswith('@') != 0:
            tag = word[1:]
            user = InstaUser.objects.filter(username=tag)
            if user:
                tags.append(tag)
    return tags