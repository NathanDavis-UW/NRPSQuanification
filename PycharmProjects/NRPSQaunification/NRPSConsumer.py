import string

from Bio.ParserSupport import AbstractConsumer


class NRPSExtractor(AbstractConsumer):

    def __init__(self):
        self.CondensationZone_list = []

    def title(self, title_info):
        title_atoms = string.split(title_info)
        new_CondensationZone = title_atoms[1]
        if new_CondensationZone not in self.species_list:
            self.CondensationZone_list.append(new_CondensationZone)