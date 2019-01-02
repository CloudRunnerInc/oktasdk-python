import json
from okta.framework.Utils import Utils


class PagedResults(object):

    def __init__(self, response, target_class=None):
        self.response = response
        self.__target_class = target_class

    def is_last_page(self):
        return not ("next" in self.response.links)

    def is_first_page(self):
        return not ("previous" in self.response.links)

    def is_only_page(self):
        return self.is_last_page() and self.is_first_page()

    @property
    def next_url(self):
        return self.response.links.get("next").get("url")

    @property
    def result(self):
        if self.__target_class is not None:
            return Utils.deserialize(self.response.text, self.__target_class)
        return json.loads(self.response.text)
