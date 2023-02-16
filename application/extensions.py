from flask_siwadoc import SiwaDoc

from application.contrib.cache import Cache
from application.contrib.openai_api import OpenAI

siwa = SiwaDoc(title="API")
openai_api = OpenAI()
cache = Cache()
