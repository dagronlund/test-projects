__author__ = 'David'

from openpyxl import *

class ObjectGenerator:

    def __init__(self, sheet):
        self.sheet = sheet

    def get_name(self, col='A'):
        name = self.sheet[col + str(self.row)].value
        if name is None:
            return None
        else:
            return name.strip().replace(' ', '_')

    def get_cell(self, col):
        return self.sheet[col + str(self.row)].value.strip()

    def write_command(self, command_file, type, ip):
        if type == 'Host':
            command_file.write('host ' + ip.split('/')[0].strip() + '\n')
        elif type == 'Range':
            command_file.write('range ' + ip.split('-')[0].strip() + ' ' + ip.split('-')[1].strip() + '\n')
        elif type == 'Network':
            command_file.write('subnet ' + ip.split('/')[0].strip() + ' ' + ip.split('/')[1].strip() + '\n')

    def write_object_commands(self, command_file):
        self.row = 2
        while self.get_name() is not None:
            command_file.write('object-network ' + self.get_name() + '\n')
            type = self.get_cell('C')  # Type
            ip = self.get_cell('B')  # IP
            self.write_command(command_file, type, ip)
            self.row += 1

    def write_group_command(self, command_file):
        self.row = 2
        while self.get_name() is not None:  # Group still exists
            command_file.write('object-group ' + self.get_name() + '\n')
            self.row += 1
            while self.get_name('B') is not None:  # Names still exist
                command_file.write('network-object ')
                type = self.get_cell('D')
                ip = self.get_cell('C')
                if ip == 'Object' or ip == 'Group':
                    command_file.write('host ' + self.get_name('C') + '\n')
                elif type == 'Host':
                    command_file.write('host ' + ip.split('/')[0].strip() + '\n')
                elif type == 'Range':
                    command_file.write(ip.split('-')[0].strip() + ' ' + ip.split('-')[1].strip() + '\n')
                elif type == 'Network':
                    command_file.write(ip.split('/')[0].strip() + ' ' + ip.split('/')[1].strip() + '\n')



object_command_file = open("C:/Users/David/Desktop/asa_object_commands.txt", 'w')
object_group_file = open("C:/Users/David/Desktop/asa_group_commands.txt", 'w')

wb = load_workbook('C:/Users/David/Desktop/Firewall Rules.xlsx')

gen = ObjectGenerator(wb['Network Objects'])
gen.write_object_commands(object_command_file)

object_command_file.close()
object_group_file.close()
