"""
Gear to analyse results from Easynido
"""
from bs4 import BeautifulSoup

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag


class EasyNidoGear(BaseGear):
    """
    Checks for EasyNido data
    """
    INTENTS = [GlobalBag.EASYNIDO_INTENT]

    def __init__(self, datastore_service):
        """

        :param datastore_service: service to manage persistent storage of data
        """
        BaseGear.__init__(self, EasyNidoGear.__name__, self.INTENTS)
        self._datastore = datastore_service

    def _check_parameters(self, params):
        return True

    def process_intent(self, intent, params):
        pass

    def parse_webservice_data(self, html_to_parse):
        """
        Given the html to parse, retrieve the different activities
        :param html_to_parse:
        :return:
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

        # Finds first high-level node, it's always a block with the day
        root = soup.find("div", class_="col-xs-12 prn pln")
        while True:
            if root is None:
                break

            # As per BeautifulSoup documentation, siblings can also be \n and
            #  empty space, so skip them
            if root == u"\n":
                root = root.next_sibling
                continue

            # First option: there is a day sub-block inside this block
            # Searching top-level class "col-xs-12 prn pln" doesn't work, it
            #  needs to search one of the sub-classes
            day = root.find("div", class_="giorno-row")
            if day is not None:
                # Day block, get the day
                for day_text in day.stripped_strings:
                    print(day_text)

            # Second option: there is an activity sub-block inside this block
            # Same here, searching top-level class "col-xs-12 ptn pbn prn pln"
            #  doesn't work, it need to search one of the sub-classes
            activity_block = root.find("div", class_="att-di-bordo")
            if activity_block is not None:
                for time in activity_block.find("div", class_="col-xs-2 ora prn").stripped_strings:
                    print(" {}".format(time))
                for activity in activity_block.find_all("div", class_="col-xs-10 info prn pls"):
                    for act_title in activity.find("span", class_="titolo-att").stripped_strings:
                        if not act_title.startswith("Ed. "):
                            print("  {}".format(act_title))
                    for act_detail in activity.find_all("span", class_="testo-black"):
                        print("   {}".format(act_detail.get_text()))

            # Move to the next block, the one with an activity
            root = root.next_sibling


        return None
