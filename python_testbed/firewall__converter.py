__author__ = 'David'

from openpyxl import *

class ObjectGenerator:

    def __init__(self, sheet):
        self.sheet = sheet

    def get_name(self):
        name = self.sheet['A' + str(self.row)].value
        if name is None:
            return None
        else:
            return name.strip().replace(' ', '_')

    def get_ip(self):
        return self.sheet['B' + str(self.row)].value.strip()

    def get_type(self):
        return self.sheet['C' + str(self.row)].value.strip()

    def get_net_type(self):
        return self.sheet['D' + str(self.row)].value.strip()

    def write_object_commands(self, command_file):
        self.row = 2
        while self.get_name() is not None:
            command_file.write('object-network ' + self.get_name() + '\n')
            type = self.get_type()
            ip = self.get_ip()
            if type == 'Host':
                command_file.write('host ' + ip.split('/')[0].strip() + '\n')
            elif type == 'Range':
                command_file.write('range ' + ip.split('-')[0].strip() + ' ' + ip.split('-')[1].strip() + '\n')
            elif type == 'Network':
                command_file.write('subnet ' + ip.split('/')[0].strip() + ' ' + ip.split('/')[1].strip() + '\n')
            self.row += 1


object_command_file = open("C:/Users/David/Desktop/asa_object_commands.txt", 'w')
object_group_file = open("C:/Users/David/Desktop/asa_group_commands.txt", 'w')

wb = load_workbook('C:/Users/David/Desktop/Firewall Rules.xlsx')

gen = ObjectGenerator(wb['Network Objects'])
gen.write_object_commands(object_command_file)

object_command_file.close()
object_group_file.close()
