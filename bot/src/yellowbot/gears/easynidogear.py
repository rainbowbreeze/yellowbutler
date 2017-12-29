"""
Gear to analyse results from Easynido
"""
import requests
from bs4 import BeautifulSoup

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag


class EasyNidoGear(BaseGear):
    """
    Checks for EasyNido data
    """
    INTENTS = [GlobalBag.EASYNIDO_INTENT]

    def __init__(self, datastore_service, email, password, idbambino):
        """

        :param datastore_service: service to manage persistent storage of data
        :type datastore_service: DatastoreService

        :param email: user email
        :type email: str

        :param password: user password
        :type password: str

        :param idbambino: id of the element to ask information for
        :type idbambino: str
        """
        BaseGear.__init__(self, EasyNidoGear.__name__, self.INTENTS)
        self._datastore = datastore_service
        self._username = email
        self._password = password
        self._idbambino = idbambino

    def _check_parameters(self, params):
        return True

    def process_intent(self, intent, params):
        webservice_data = self._obtain_webservice_data()
        if not webservice_data:
            return "Something wrong happened query the kindergarten service ¯\_(ツ)_/¯ "
        else:
            return self.parse_webservice_data(webservice_data)

    def _obtain_webservice_data(self):
        """
        Reads data from webservice

        :return: None if it was some error, otherwise the data
        :rtype: str
        """

        # Useful links on requests library
        #  How to deal with session: http://docs.python-requests.org/en/master/user/advanced/
        #  How to deal with cookies: http://docs.python-requests.org/en/master/api/#api-cookies

        # This will make sure the session is closed as soon as the with block
        #  is exited, even if unhandled exceptions occurred.
        with requests.session() as session:
            # Login
            r = session.post(
                "https://easynido.it/login",
                data={
                    'email': self._username,
                    'pwd': self._password
                }
            )
            # if the login fail, result.url is https://easynido.it/it/login
            login_success = r.ok and "https://easynido.it/familiare/bacheca" == r.url

            if not login_success:
                return None

            # Get data
            r = session.post(
                "https://easynido.it/genitore/diarioBordocontent",
                data={
                    'idbambino': self._idbambino,
                    'data': "",
                    'mod': "tutto",
                    'page': 1,
                    'maxRecords': 6
                }
            )
            if r.ok and r.text and r.text.startswith("<script>"):
                # finally, we have the information we need
                return r.text

        return None

    def parse_webservice_data(self, html_to_parse):
        """
        Given the html to parse, retrieve the different activities

        :param html_to_parse: EasyNido webserver call to parse
        :type html_to_parse: str

        :return: a string with a list of events
        :rtype: str
        """
        soup = BeautifulSoup(html_to_parse, 'html.parser')
        # Days and activities tag are all at the same level in the doc
        #  structure. Sometimes there is a day, then activities within that
        #  day follows till when another day is encountered and so on.
        # Days are inside the high-level tag <div class="col-xs-12 prn pln">
        #  and the child tag <div class="giorno-row">
        # Activities inside the high level tag <div class="col-xs-12 ptn pbn prn pln">
        #   As children at the same level:
        #   there is time, in the tag <div class="col-xs-2 ora prn">
        #   there is activity, in the tag <div class="col-xs-10 info prn pls">
        #     As children at the same level:
        #     activity type is in the child tag <span class="titolo-att">
        #       first one is the activity name, second one the text "Ed. Asilo Nido e Scuola" etc
        #     several <span class="testo-black">, with more info on the activity

        # Find all the days
        # print("----------")
        # for day in soup.find_all("div", class_="giorno-row"):
        #     print(day.em.string)
        # print("----------")
        #
        # # Find all the activities, but not connected with days
        # for activity_block in soup.find_all("div", class_="col-xs-12 ptn pbn prn pln"):
        #     for time in activity_block.find("div", class_="col-xs-2 ora prn").stripped_strings:
        #         print("Time: {}".format(time))
        #     for activity in activity_block.find_all("div", class_="col-xs-10 info prn pls"):
        #         for act_title in activity.find("span", class_="titolo-att").stripped_strings:
        #             print("Activity: {}".format(act_title))
        #         for act_detail in activity.find_all("span", class_="testo-black"):
        #             print("  {}".format(act_detail.get_text()))
        # print("----------")

        events = []
        # Finds first high-level node, it's always a block with the day
        root = soup.find("div", class_="col-xs-12 prn pln")
        while True:
            if root is None:
                break

            # As per BeautifulSoup documentation, siblings can also be \n and
            #  empty space, so skip them.
            # More at https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html#next-sibling-and-previous-sibling
            if u"\n" == root:
                root = root.next_sibling
                continue

            # First option: there is a day sub-block inside this block
            # Searching top-level class "col-xs-12 prn pln" doesn't work, it
            #  needs to search one of the sub-classes
            day = root.find("div", class_="giorno-row")
            if day is not None:
                # Day block, get the day
                for day_text in day.stripped_strings:
                    events.append(day_text)

            # Second option: there is an activity sub-block inside this block
            # Same here, searching top-level class "col-xs-12 ptn pbn prn pln"
            #  doesn't work, it need to search one of the sub-classes
            activity_block = root.find("div", class_="att-di-bordo")
            if activity_block is not None:
                for time in activity_block.find("div", class_="col-xs-2 ora prn").stripped_strings:
                    events.append(" {}".format(time))
                for activity in activity_block.find_all("div", class_="col-xs-10 info prn pls"):
                    for act_title in activity.find("span", class_="titolo-att").stripped_strings:
                        if not act_title.startswith("Ed. "):
                            events.append("  {}".format(act_title))
                    for act_detail in activity.find_all("span", class_="testo-black"):
                        events.append("   {}".format(act_detail.get_text()))

            # Move to the next block, the one with an activity
            root = root.next_sibling

        print("\n".join(events))
        return "\n".join(events)
