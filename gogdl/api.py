import logging
import requests
import json
from multiprocessing import cpu_count
from gogdl.dl.dl_utils import get_zlib_encoded
import gogdl.constants as constants

class ApiHandler():
    def __init__(self, token):
        self.logger = logging.getLogger("API")
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_maxsize=cpu_count())
        self.session.mount("https://", adapter)
        self.session.headers = {
            "Authorization": f"Bearer {token}"
        }

    def get_item_data(self, id):
        url = f'{constants.GOG_API}/products/{id}?expanded=changelog'
        response = self.session.get(url)
        self.logger.debug(url)
        if response.ok:
            return response.json()    

    def get_game_details(self, id):
        url = f'{constants.GOG_EMBED}/account/gameDetails/{id}.json'
        response = self.session.get(url)
        self.logger.debug(url)
        if response.ok:
            return response.json()    

    def get_dependenices_list(self):
        self.logger.info("Getting Dependencies repository")
        response = self.session.get(constants.DEPENDENCIES_URL)
        if not response.ok:
            return None
        
        json_data = json.loads(response.content)
        if 'repository_manifest' in json_data:
            self.logger.info("Getting repository manifest")
            return get_zlib_encoded(self, str(json_data['repository_manifest']))

    def does_user_own(self, id):
        game_details = self.get_game_details(id)
        return game_details != []