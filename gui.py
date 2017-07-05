import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import geneticalgorithm as ga
from tkinter import *
from tkinter import filedialog
import os
import threading
import copy
import population as pop
import settings
import time

matplotlib.use('TkAgg')
root = Tk()

class GUI(object):
    def __init__(self, master):
        self.ga = ga.GeneticAlgorithm()
        self.file =None
        self.master = master
        self.master.title('TSP Optimalizer')
        self.init_map(master)
        self.frame = Frame(master)
        self.frame = Frame(width=200, height=500)
        self.frame.grid(row=1, column=2, columnspan=2, rowspan=2, sticky=(E, W, N, S))
        self.lb_file = Label(master, text=self.file)
        self.lb_file.grid(row=0, column=1, sticky=W)
        self.bt_open_file = Button(master, text='Open file', command=self.open_file,height = 1, width = 10)
        self.bt_open_file.grid(row=0, column=2, sticky=W)
        self.lb_initial_length = Label(master, text='Počiatočná dĺžka:  ----', fg='blue', font=('times', 20, 'bold'))
        self.lb_initial_length.grid(row=2, column=4, sticky=E)
        self.lb_best_length = Label(master, text='Najkratšia:  ----', fg='red', font=('times', 20, 'bold'))
        self.lb_best_length.grid(row=3, column=4, sticky=E)
        self.lb_current_length = Label(master, text='Aktuálna dĺžka:  ----', font=('times', 20, 'bold'))
        self.lb_current_length.grid(row=4, column=4, sticky=E)
        self.lb_current_generation = Label(master, text='Generácia:  ---', font=('times', 25, 'bold'))
        self.lb_current_generation.grid(row=1, column=4, sticky=E)
        #self.lb_time = Label(master, text='Čas:  ----', fg='red', font=('times', 20, 'bold'))
        #self.lb_time.grid(row=5, column=3, sticky=E)





    def open_file(self):
        self.file = filedialog.askopenfile()
        self.lb_file.config(text='Otvorený súbor: ' + self.file.name)
        self.master.title('TSP Optimalizer ' + self.file.name)
        self.bt_open_file.config(state='disabled')
        settings.initialize_variables()
        self.init_settings_tools(self.master)



    def init_map(self, master):

        b = Figure(figsize=(8, 6), dpi=100)
        ac = b.add_subplot(111)
        ac.plot(10, 10)
        ac.grid(True)
        canvas = FigureCanvasTkAgg(b, master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=1, rowspan=5, sticky=W)

    def init_settings_tools(self, master):
        self.lb_population_size= Label(master, text='Veľkosť populácie',font=('times', 15, 'bold'))
        self.lb_population_size.grid(row=6, column=1, sticky=(S,E))
        self.sc_population_size = Scale(master, from_=100, to=2000,resolution = 10, orient=HORIZONTAL)
        self.sc_population_size.grid(row=7, column=1, sticky=(N,E))
        self.lb_generation_count = Label(master, text='Počet generácií', font=('times', 15, 'bold'))
        self.lb_generation_count.grid(row=6, column=2, sticky=S)
        self.sc_generations_count = Scale(master, from_=100, to=2000,resolution = 10, orient=HORIZONTAL)
        self.sc_generations_count.grid(row=7, column=2, sticky=N)
        self.var_s = StringVar(self.frame)
        self.var_s.set("roulette")
        self.var_c = StringVar(self.frame)
        self.var_c.set("oox")
        self.var_m = StringVar(self.frame)
        self.var_m.set("swap")
        self.opt_selection = OptionMenu(master,self.var_s, "tournament", "roulette")
        self.opt_selection.config(width = 15)
        self.opt_selection.grid(row=5, column=3, sticky=W)
        self.opt_crossover = OptionMenu(master, self.var_c, "oox", "pmx")
        self.opt_crossover.config(width=15)
        self.opt_crossover.grid(row=6, column=3, sticky=W)
        self.opt_mutation = OptionMenu(master, self.var_m, "swap", "inverse", "psm")
        self.opt_mutation.config(width=15)
        self.opt_mutation.grid(row=7, column=3, sticky=W)



        self.bt_open_file = Button(master, text='Počítať',font=('times', 20, 'bold'), command=self.loop, height = 5, width = 15)
        self.bt_open_file.grid(row=5, column=4, rowspan=3, sticky=E)

    def disable_setting_tools(self):
        self.sc_generations_count.config(state='disabled')
        self.sc_population_size.config(state='disabled')
        self.bt_open_file.config(state='disabled')
        self.opt_selection.config(state='disabled')
        self.opt_crossover.config(state='disabled')
        self.opt_mutation.config(state='disabled')

    def draw_route(self, route):
        x = []
        y = []
        for i in route.route:
            x.append(i.x)
            y.append(i.y)
        plt.ion()
        self.a.cla()
        self.a.plot(x, y, 'ro')
        self.a.plot(x, y, 'b-')
        self.canvas.draw()

    def draw_cities(self, cities):
        x= []
        y= []
        for i in cities.route:
            x.append(i.x)
            y.append(i.y)

        plt.ion()

        self.f = Figure(figsize=(8, 6), dpi=100)
        self.a = self.f.add_subplot(111, navigate=True)
        self.a.plot(x, y, 'ro')
        self.a.set_title('Current best tour')
        self.a.set_xlabel('X axis coordinates')
        self.a.set_ylabel('Y axis coordinates')
        self.a.grid(True)
        self.canvas = FigureCanvasTkAgg(self.f, master=root)
        self.canvas.get_tk_widget().grid(row=1, column=1,rowspan=5, sticky=W)
        self.canvas.draw()
        self.canvas.show()

    def update_initial_length(self, length):
        self.lb_initial_length.config(text='Počiatočná dĺžka:  '+str(length))

    def update_best_length(self, length):
        self.lb_best_length.config(text='Najkratšia:  '+str(length))

    def update_current_length(self, length):
        self.lb_current_length.config(text='Aktuálna dĺžka:  '+str(length))

    def update_current_generation(self, generation):
        self.lb_current_generation.config(text='Generácia:  '+str(generation))

    #def show_time(self, time):
     #   self.lb_time.config(text='Čas:  {0:.1f}s' .format(time))







    def loop(self):
        self.disable_setting_tools()
        settings.crossover = self.var_c.get()
        settings.mutation = self.var_m.get()
        settings.selection = self.var_s.get()
        settings.population_size = self.sc_population_size.get()
        settings.generation_size = self.sc_generations_count.get()
        def callback():

            self.ga.initialize_genens(self.file.name)
            the_population = pop.Population(settings.population_size, True)
            if the_population.fittest.genes_validation() == False:
                raise NameError('Multiple cities with same name. Check cities.')
                return

            initial_length = the_population.fittest.length
            fittest_chromosome = pop.Chromosome()
            self.draw_cities(the_population.fittest)
            self.draw_route(fittest_chromosome)
            self.update_initial_length(initial_length)
            self.update_best_length(fittest_chromosome.length)
            self.update_current_length(the_population.fittest.length)

            i=1
            while i < settings.generation_size:
                the_population = self.ga.evolve(the_population)
                self.update_current_length(the_population.get_fittest().length)
                self.update_current_generation(i)
                if the_population.fittest.length < fittest_chromosome.length:
                    fittest_chromosome = copy.deepcopy(the_population.get_fittest())
                    self.update_best_length(fittest_chromosome.length)
                    self.draw_route(fittest_chromosome)
                i +=1



        t = threading.Thread(target=callback)
        t.start()



top = GUI(root)
root.mainloop()