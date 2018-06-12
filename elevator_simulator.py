__author__ = 'Tomasz Lukos'
"""This is elevator simulation with Pygame. I will create 3 classes: Customer, Elevator and Building. When we start
program then pygame will initialize and user will be asked to enter number of floors and number of customers. Only valid
inputs will be accepted. After that the simulation will start, at the end the user will have choice to finish or do new
simulation. The user can do as many simulations as he/she wants. At the end of each simulation pagame display statistics
which involve number of customers, floors and number of elevator movements to bring all customers to their destination
this is just additional comment
floors. The user can exit simulation at any stage- by pressing x on pygame window or by using esc button"""

import pygame, os, sys, string
from random import *
from pygame.locals import *
import ctypes
# I had to use one global variable to position the window correctly. It did not work properly when it was part of main
os.environ['SDL_VIDEO_WINDOW_POS'] = '50, 50'


class Customer():
    def __init__(self, current_floor, dest_floor, cust_id, in_elevator=False, reached_dest=False, goes_back=False):
        """ creates new instance of customer with customer current floor and destination floor"""
        self.current_floor = current_floor
        self.dest_floor = dest_floor
        self.cust_id = cust_id
        self.in_elevator = in_elevator
        self.reached_dest = reached_dest
        self.goes_back = goes_back

    def __str__(self):
        """ print customer details """
        return "ID:{} ,current floor:{} ,destination floor:{}".format(self.cust_id, self.current_floor, self.dest_floor)

    def __repr__(self):
        """ displays customer details in python console """
        return self.__str__()


class Elevator():
    def __init__(self, num_floor, cur_floor=0, direction="up", max_capacity=6):
        """ create new instance of elevator with number of floors the elevator can work for"""
        self.num_floor = int(num_floor)
        self.cur_floor = int(cur_floor)
        self.direction = direction
        self.in_elev_list = []
        self.max_capacity = max_capacity
        self.total_moves = 0

    def __str__(self):
        """ print elevator details(number of floors and customers in elevator) """
        return 'Elevator for building with {} floors, currently {} customers in it'.\
            format(self.num_floor, len(self.in_elev_list))

    def __repr__(self):
        """ displays elevator details in python console """
        return self.__str__()

    def move(self):
        """ moves elevator up and down """
        if self.cur_floor == 0:
            self.cur_floor += 1
            self.direction = 'up'
        elif self.cur_floor == self.num_floor - 1:
            self.cur_floor -= 1
            self.direction = 'down'
        elif self.cur_floor < self.num_floor - 1 and self.direction == 'up':
            self.cur_floor += 1
        elif self.cur_floor < self.num_floor - 1 and self.direction == 'down':
            self.cur_floor -= 1
        self.total_moves += 1

    def reg_cust(self, customer):
        """ register new customer to elevator """
        self.in_elev_list.append(customer.cust_id)

    def remove_cust(self, customer):
        """ remove customer from elevator """
        self.in_elev_list.remove(customer.cust_id)


class Building():
    # I had to use below class arguments to use them BEFORE instance of building class was created
    colors = {"BLACK": (0, 0, 0), "BLUE": (0, 0, 255), "WHITE": (255, 255, 255), "ORANGE": (255, 165, 0),
              "RED": (255, 0, 0), "GREEN": (0, 255, 0)}
    # I hope that below try/except will enable my program to work on Linux- as I only tested it on windows 8
    x = 2.5
    y = 2.65
    try:
        user32 = ctypes.windll.user32
        screenWidth = user32.GetSystemMetrics(0)
        screenHeight = user32.GetSystemMetrics(1)
    except:
        try:  # Platforms supported by GTK3, Fx Linux/BSD
            from gi.repository import Gdk
            screen = Gdk.Screen.get_default()
            screenWidth = screen.get_width()
            screenHeight= screen.get_height()
        except:  # default value in case that OS is not windows or linux
            screenWidth = 1440
            screenHeight = 800
        x = 2.6
        y = 3.1
    print(screenWidth, screenHeight , x , y )
    #the program will adjust window to the size of the monitor- I tested it on 3 different monitors and it worked fine
    width = int((screenWidth - 100) / 2)
    size = (width, screenHeight - 100)
    screen = pygame.display.set_mode(size)
    max_number_floors = int((screenHeight - 100) / 4)
    if width < 640:
        width = 640


    def __init__(self, num_floor, num_customer, elevator):
        """ create new building, takes 3 arguments: number of customers, number of floors and elevator """
        self.num_floor = num_floor
        self.num_customer = num_customer
        self.elevator = elevator
        self.my_build_list = []
        self.raw = []
        self.customer_dict = {}
        self.customer_list = []
        self.floor_size = 0
        #initialize customers in building
        self.init_customers()
        # make sure that elevator max capacity is not too big or too small
        if self.elevator.max_capacity > self.floor_size:
            self.elevator.max_capacity = self.floor_size
        if self.elevator.max_capacity >= self.num_customer:
            self.elevator.max_capacity = self.num_customer
        if self.elevator.max_capacity < 4:
            self.elevator.max_capacity = 4
        #creating list of lists- "E"- elevator, customer ID- customers, "_"- empty floor space and "."- empty elevator
        for i in range(self.num_floor):
            if i == self.elevator.cur_floor:
                self.raw += ['E'] * self.elevator.max_capacity
                self.raw += ['_'] * self.floor_size
                self.my_build_list.append(self.raw)
                self.raw = []
            else:
                self.raw += ['.'] * self.elevator.max_capacity
                self.raw += ['_'] * self.floor_size
                self.my_build_list.append(self.raw)
                self.raw = []
            for customer in self.customer_list:
                if customer.current_floor == i:
                    self.my_build_list[i][self.my_build_list[i].index('_')] = '{}'.format(customer.cust_id)

    def __str__(self):
        """ print building as a string """
        build_str = ''
        for i in reversed(range(len(self.my_build_list))):
            for j in range(len(self.my_build_list[i])):
                if len(str(self.my_build_list[i][j])) == 1:
                    build_str += '  {}  '.format(str(self.my_build_list[i][j]))
                elif len(str(self.my_build_list[i][j])) == 2:
                    build_str += ' {}  '.format(str(self.my_build_list[i][j]))
                else:
                    build_str += ' {} '.format(str(self.my_build_list[i][j]))
            build_str += '\n'
        return build_str

    def __repr__(self):
        """ display building in python console """
        return self.__str__()

    def init_customers(self):
        """ initialize customers into a building """
        print("Initializing {} customers in the building".format(self.num_customer))
        for i in range(self.num_customer):
            cust_curr_floor = randint(0, self.num_floor - 1)
            cust_dest_floor = randint(0, self.num_floor - 1)
            #make sure that current floor does not equal to destination floor
            while True:
                if cust_dest_floor == cust_curr_floor:
                    cust_dest_floor = randint(0, self.num_floor - 1)
                else:
                    break
            try:
                self.customer_dict[cust_curr_floor] += 1
            except KeyError:
                self.customer_dict[cust_curr_floor] = 1
            try:
                self.customer_dict[cust_dest_floor] += 1
            except KeyError:
                self.customer_dict[cust_dest_floor] = 1
            self.new_customer = Customer(cust_curr_floor, cust_dest_floor, i)
            self.customer_list.append(self.new_customer)
            print(self.new_customer)
        #I used dictionary to create optimal floor size- just to match maximum number of customers
        for i in self.customer_dict.values():
            if i > self.floor_size:
                self.floor_size = i
                if self.floor_size < 4:
                    self.floor_size = 4

    def update_elevator(self):
        """ updates customers in elevator """
        self.my_build_list[self.elevator.cur_floor] = \
            self.elevator.in_elev_list[:len(self.elevator.in_elev_list)] + \
            ['E'] * (self.elevator.max_capacity - len(self.elevator.in_elev_list)) + \
            self.my_build_list[self.elevator.cur_floor][self.elevator.max_capacity:]

    def update_pygame(self, screen, row, column, line_size, indent, size):
        """ updates pygame display """
        x = line_size
        #some completed calculations to draw my pagame picture
        for i in range(len(self.my_build_list)):
            for j in range(len(self.my_build_list[i])):
                c = self.colors
                #all drawing is based on rectangles- use different colors and sizes
                if self.my_build_list[i][j] == '.':
                    pygame.draw.rect(screen, c["BLACK"], (j * row, (size[1] - x) - (i * column), row, x))
                    pygame.draw.rect(screen, c["BLACK"], (j * row + indent, (size[1] - x) - (i * column) - x, x, x))
                elif self.my_build_list[i][j] == 'E':
                    pygame.draw.rect(screen, c["GREEN"], (j * row, (size[1] - x) - (i * column), row, x))
                    pygame.draw.rect(screen, c["BLACK"], (j * row + indent, (size[1] - x) - (i * column) - x, x, x))
                elif self.my_build_list[i][j] == '_':
                    pygame.draw.rect(screen, c["BLUE"], (j * row, (size[1] - x) - (i * column), row, x))
                    pygame.draw.rect(screen, c["BLACK"], (j * row + indent, (size[1] - x) - (i * column) - x, x, x))
                else:
                    customer = self.customer_list[int(self.my_build_list[i][j])]
                    col = c["RED"]
                    if customer.reached_dest:
                        col = c["WHITE"]
                    elif customer.in_elevator:
                        col = c["ORANGE"]
                    if j < self.elevator.max_capacity:
                        pygame.draw.rect(screen, c["GREEN"], (j * row, (size[1] - x) - (i * column), row, x))
                        pygame.draw.rect(screen, col, (j * row + indent, (size[1] - x) - (i * column) - x, x, x))
                    else:
                        pygame.draw.rect(screen, c["BLUE"], (j * row, (size[1] - x) - (i * column), row, x))
                        pygame.draw.rect(screen, col, (j * row + indent, (size[1] - x) - (i * column) - x, x, x))

    @staticmethod
    def pygame_type_integer(display_text, min_value, max_value, w, x, y, z):
        """method to enter valid integers in pygame(number of customers or floors), takes 7 arguments"""
        my_font2 = pygame.font.SysFont('Arial', int(Building.max_number_floors / 6.66))
        my_input = ""
        res = 0
        Building.screen.blit(my_font2.render("{}".format(display_text).format(max_value), 1,
                                             Building.colors["GREEN"]), (5, z))
        while not res:
            pygame.display.update()
            for event in pygame.event.get():
                #user can exit whenever he/she wants
                if event.type == QUIT or (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                    sys.exit()
                #few scenarios to deal with user input
                if event.type == KEYDOWN:
                    if pygame.key.name(event.key) != "return" and pygame.key.name(event.key) in\
                            string.digits + string.ascii_letters + string.punctuation:
                        my_input += pygame.key.name(event.key)
                        label16 = my_font2.render(my_input, 1, Building.colors["GREEN"])
                        pygame.draw.rect(Building.screen, Building.colors["BLACK"], [y, z, 740, 70])
                        pygame.draw.rect(Building.screen, Building.colors["BLACK"], [5, x, 740, 70])
                        Building.screen.blit(label16, (y, z))
                        pygame.display.update()
                    elif pygame.key.name(event.key) == "backspace":
                        my_input = my_input[:-1]
                        pygame.draw.rect(Building.screen, Building.colors["BLACK"], [y, z, 400, 70])
                        label16 = my_font2.render(my_input, 1, Building.colors["GREEN"])
                        Building.screen.blit(label16, (y, z))
                        pygame.display.update()
                    elif pygame.key.name(event.key) == "space":
                        my_input += " "
                        pygame.draw.rect(Building.screen, Building.colors["BLACK"], [w, z, 400, 70])
                        label16 = my_font2.render(my_input, 1, Building.colors["GREEN"])
                        Building.screen.blit(label16, (y, z))
                        pygame.display.update()
                    elif pygame.key.name(event.key) == "return" and len(my_input) > 0:
                        try:
                            label18 = my_font2.render("Invalid input, try again...", 1, Building.colors["RED"])
                            result = int(my_input)
                            if min_value > result or result > max_value:
                                raise ValueError
                            res += 1
                        except ValueError:
                            my_input = ""
                            Building.screen.blit(label18, (5, x))
                            pygame.display.update()
                    elif pygame.key.name(event.key) == "return" and len(my_input) == 0:
                        label18 = my_font2.render("Invalid input, try again...", 1, Building.colors["RED"])
                        pygame.draw.rect(Building.screen,Building.colors["BLACK"], [y, z, 740, 70])
                        my_input = ""
                        Building.screen.blit(label18, (5, y))
                        pygame.display.update()
        return result

    @staticmethod
    def pygame_start():
        """method to start initial pygame screen"""
        Building.screen.fill(Building.colors["BLACK"])
        pygame.display.set_caption('Elevator simulation')
        pygame.init()
        #few basic values to be display on the screen
        my_font = pygame.font.SysFont('Arial', int(Building.max_number_floors / 10))
        my_font2 = pygame.font.SysFont('Arial', int(Building.max_number_floors / 6.66))
        label0 = my_font2.render("THIS IS ELEVATOR SIMULATION", 1, Building.colors["GREEN"])
        label2 = my_font2.render("The program will run until...", 1, Building.colors["GREEN"])
        label3 = my_font2.render("...all customers reach their destination's floors", 1, Building.colors["GREEN"])
        label9 = my_font.render("Press any key to start..............", 1, Building.colors["GREEN"])
        Building.screen.blit(label0, (55, Building.max_number_floors))
        Building.screen.blit(label2, (55, int(Building.max_number_floors * 1.5)))
        Building.screen.blit(label3, (55, int(Building.max_number_floors * 2)))
        Building.screen.blit(label9, (55, int(Building.max_number_floors * 2.5)))
        pygame.display.update()
        res = 0
        #the simulation will start when user will press any key, there is also option to exit
        while not res:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                    sys.exit()
                elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    res = 1
        Building.screen.fill(Building.colors["BLACK"])

    def run(self):
        """ runs the simulation until all customers reach their destination's floors """
        #different time delays depending on customer number
        if self.num_customer < 1000:
            time_delay = 200
        elif self.num_customer < 5000:
            time_delay = 100
        else:
            time_delay = 0
        k = self.max_number_floors
        #all sizes are relevant to monitor size, they also adjust to number of floors and width of floor
        my_font2 = pygame.font.SysFont('Arial', int(k / 6.66))
        size_0 = int(self.width - (self.width % (self.floor_size + self.elevator.max_capacity)))
        size_1 = int((self.screenHeight - 100) - ((self.screenHeight - 100) % self.num_floor))
        self.size = (size_0, size_1)
        if self.num_customer / self.num_floor >= 50:
            size_0 = int((self.screenWidth - 100) - ((self.screenWidth - 100) % (self.floor_size + self.
                                                                                 elevator.max_capacity)))
            self.size = (size_0, size_1)
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(self.colors["BLACK"])
        pygame.display.update()
        pygame.time.delay(time_delay)
        self.screen.fill(self.colors["BLACK"])
        row = self.size[0] // (self.floor_size + self.elevator.max_capacity)
        column = self.size[1] // self.num_floor
        line_size = column / 3
        #some calculation to make sure that simulator will display nicely
        if line_size > 15:
            line_size = 15
        indent = int(0.5 * line_size)
        if indent == 0:
            indent = 1
        if self.num_customer > 10 * self.num_floor:
            if self.num_customer / self.num_floor < int(k / 10) and self.num_floor <= int(k / 5):
                line_size = 9
                indent = 3
            elif self.num_customer / self.num_floor < int(k / 4.5):
                line_size = 4
                indent = 2
            elif self.num_customer / self.num_floor < int(k / 2):
                line_size = 3
                indent = 1
            else:
                line_size = 2
                indent = 1
        if line_size < 3 and self.num_floor <= int(k / 2):
            line_size = 3
        if line_size <= 4 and self.num_floor > int(k / 2):
            line_size = 2
        counter = 0
        #start of my simulation
        while counter < len(self.customer_list):
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                    sys.exit()
            self.update_pygame(self.screen, row, column, line_size, indent, self.size)
            pygame.display.update()
            pygame.time.delay(time_delay)
            #had to use copies as in other case removing customers would affect my index
            copy_in_elev_list = self.elevator.in_elev_list[:]
            #first we check for customers who are in elevator and reached their destination floor
            for i in copy_in_elev_list:
                if self.customer_list[i].dest_floor == self.elevator.cur_floor:
                    self.customer_list[i].reached_dest = True
                    self.customer_list[i].in_elevator = False
                    self.elevator.remove_cust(self.customer_list[i])
                    j = 1
                    while True:
                        if self.my_build_list[self.elevator.cur_floor][-j] == '_':
                            self.my_build_list[self.elevator.cur_floor][-j] = '{}'.format(self.customer_list[i].cust_id)
                            break
                        else:
                            j += 1
                    counter += 1
                self.update_elevator()
            #we check for customers who want to enter elevator
            for customer in self.customer_list:
                if customer.current_floor == self.elevator.cur_floor and not customer.in_elevator and \
                        not customer.reached_dest:
                    if len(self.elevator.in_elev_list) < self.elevator.max_capacity:
                        self.elevator.reg_cust(customer)
                        customer.in_elevator = True
                        if len(self.elevator.in_elev_list) > 0:
                            for i in self.elevator.in_elev_list:
                                if self.customer_list[i].current_floor == self.elevator.cur_floor and \
                                        not self.customer_list[i].goes_back:
                                    self.my_build_list[self.elevator.cur_floor][self.my_build_list[
                                        self.elevator.cur_floor].index('{}'.format(i))] = '_'
                                    self.customer_list[i].goes_back = True
                                    self.update_elevator()
                    else:
                        self.my_build_list[self.elevator.cur_floor][self.my_build_list[self.elevator.cur_floor].
                                                                    index('{}'.format(customer.cust_id))] = '_'
                        self.my_build_list[self.elevator.cur_floor][self.my_build_list[self.elevator.cur_floor].
                                                                    index('_')] = '{}'.format(customer.cust_id)
            self.update_pygame(self.screen, row, column, line_size, indent, self.size)
            pygame.display.update()  # updates the screen
            pygame.time.delay(time_delay)
            #update my build list with empty elevator + floor as elevator will move
            self.my_build_list[self.elevator.cur_floor] = ['.'] * self.\
                elevator.max_capacity + self.my_build_list[self.elevator.cur_floor][self.elevator.max_capacity:]
            if counter < len(self.customer_list):
                self.elevator.move()
            self.update_elevator()
        #print report, not really needed with pygame but I think it is nice to have
        print("*" * 80)
        print("Simulation completed.")
        print("Elevator with maximum capacity of {} customer(s).".format(self.elevator.max_capacity))
        print("Building with {} floors and {} customers.".format(self.num_floor, self.num_customer))
        print("Elevator moved {} times to bring all customers to their destination's floors.".format
              (self.elevator.total_moves))
        print("*" * 80)
        pygame.time.delay(3000)
        #below section will display simulation report in pygame
        self.size = (self.width, self.screenHeight - 100)
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(self.colors["BLACK"])
        self.screen.blit(my_font2.render("Simulation completed.", 1, (self.colors["GREEN"])),
                         (int(k / 3.64),int(k / 2)))
        self.screen.blit(my_font2.render("Elevator with maximum capacity of {} customer(s).".format(
            self.elevator.max_capacity), 1, (self.colors["GREEN"])), (int(k / 3.64), k))
        self.screen.blit(my_font2.render("Building with {} floors and {} customers.".format(
            self.num_floor, self.num_customer), 1, (self.colors["GREEN"])), (int(k / 3.64), int(k * 1.5)))
        self.screen.blit(my_font2.render("Elevator moved {} times to bring...".format(
            self.elevator.total_moves), 1, (self.colors["GREEN"])), (int(k / 3.64), int(k * 2)))
        self.screen.blit(my_font2.render("... all customers to their destination's floors.", 1,
                                         (self.colors["GREEN"])), (int(k / 3.64), int(k * 2.5)))
        self.screen.blit(my_font2.render("Press Enter for new simulation or esc to quit", 1,
                                         self.colors["RED"]), (int(k / 3.64), int(k * 3)))
        pygame.display.update()
        #option for user-play again or exit
        main_cnt = 0
        while not main_cnt :
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)or event.type == QUIT:
                    sys.exit()
                elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                    main_cnt += 1
                else:
                    continue
        #if user pressed return then next simulation will start
        if main_cnt == 1:
            main()


def main():
    """ main method for user to input number of floors and customers, initialize building and start run method """
    x = Building.max_number_floors
    Building.pygame_start()
    Building.int_floor = Building.pygame_type_integer(
        display_text="enter number of floors(min 2, max {}):".format(x),
        min_value=2, max_value=x, x=int(x * 1.5), y=int(x * Building.x), z=x, w=int(x * 2.5))
    Building.int_customers = Building.pygame_type_integer(
        display_text="enter number of customers(min 1, max {}):",
        min_value=1, max_value=Building.int_floor * 100, x=int(x * 2.5), y=int(x * Building.y), z=int(x * 2), w=int(x * 2.25))
    new_building = Building(Building.int_floor, Building.int_customers, Elevator(Building.int_floor))
    new_building.run()

if __name__ == "__main__":
    main()

