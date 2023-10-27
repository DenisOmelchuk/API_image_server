import random
import string


def get_upload_path(instance, filename):
    return os.path.join('images', str(instance.pk), filename)

def generate_random_link(base_url):
    characters = string.ascii_letters + string.digits
    url = ''.join(random.choice(characters) for _ in range(15))
    return base_url + url + '/'