'''
@filename: spectroscopy
@author: Johirul Islam
@created: 05.11.2017
@description: 
    A very simple graphical user interface to plot spectroscopy.
    
    In electron spectroscopy matter is examined by radiating it 
    with a bright light and measuring the kinetic energy of electrons 
    that come off it. When the photonic energy of light and kinetic 
    energy of the electrons are known, they can be used to derive the 
    amount of force that was required to break off the electrons. This 
    provides valuable information about the matter's electron structure, 
    and its chemical and physical properties. This phenomenon where 
    photons break off electrons is called photoionization, and the 
    broken off electrons are called photoelectrons.
    
    This project requires two third party libraries: numpy and matplotlib. 
    There are multiple ways to install them. Windows installers 
    can be found for both, and can also be installed them using pip. There 
    are also various full stack installers available in the internet (full 
    stack means they install Python along with a bunch of libraries, usually 
    replacing "generic" Python installation). 
    :numpy::
    :matplotlib::
'''


from tkinter import *
from tkinter import filedialog, messagebox
from os import walk
import numpy as np
import matplotlib.pyplot as plt
import os

class Spectroscopy():
    """
    Initializing spectroscopy ...
    Please wait ...
    """
    print(__name__, __doc__)
    
    #class valribles
    widthpixels = 210 
    heightpixels = 105
    title = "spectrocopy"
    x_min = 0.0
    x_max = 100.0
    required_extension = '.txt'
    data = []
    
    def __init__(self, gui):
        '''
        Congratulations! 
        Spectroscopy initialized successfully!! ...
        '''
        
        self.setWindowTitle(gui)
        self.setNonResizableWindow(gui)
        self.x_ranges(gui)
        self.setLoadButtons(gui)
        self.setWindowAtCenter(gui)
        
        
        print(self.__init__.__name__, self.__init__.__doc__)
        
    def setWindowAtCenter(self, gui):        
        '''
        Placing the window into the center of the screen ...
        '''
        print(self.setWindowAtCenter.__name__, self.setWindowAtCenter.__doc__)
        
        gui.update_idletasks()
        w = gui.winfo_screenwidth()
        h = gui.winfo_screenheight()
        size = tuple(int(_) for _ in gui.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        gui.geometry("%dx%d+%d+%d" % (size + (x, y)))
        
    def setWindowTitle(self, gui):
        '''
        Setting the window title ...
        '''
        print(self.setWindowTitle.__name__, self.setWindowTitle.__doc__)
        gui.title(self.title)
        
    def setNonResizableWindow(self, gui):
        '''
        Setting the window to non resizable ...
        '''
        print(self.setNonResizableWindow.__name__, self.setNonResizableWindow.__doc__)
        
        gui.geometry('{}x{}'.format(self.widthpixels, self.heightpixels))
        gui.resizable(width=False, height=False)
        
    def setLoadButtons(self, gui):
        '''
        Placing Load Data & Plot Data Buttons ...
        '''
        print(self.setLoadButtons.__name__, self.setLoadButtons.__doc__)
        
        Button(gui, text="Load Data", command=lambda:self.loaddata()).grid(row=4, column=0, sticky=W, padx=5, pady=5)
        Button(gui, text="Plot Data", command=self.plotdata).grid(row=4, column=1, sticky=E, padx=5, pady=5)
        
    def x_ranges(self, gui):
        '''
        Placing x ranges ... 
        '''
        print(self.x_ranges.__name__, self.x_ranges.__doc__)
        
        # set x-min & x-max label into the gui
        Label(gui, text="x-min").grid(row=0, column = 0, padx=5, pady=5)
        Label(gui, text="x-max").grid(row=2, column = 0, padx=5, pady=5)
        
        # validate x-min & x-max
        v_x_min = gui.register(self.validate_x_min) 
        v_x_max = gui.register(self.validate_x_max) 
        
        # set x-min & x-max input field
        self.x_min_input = Entry(gui, validate="key", validatecommand=(v_x_min, '%P'))
        self.x_max_input = Entry(gui, validate="key", validatecommand=(v_x_max, '%P'))
        
        # set x ranges according to x-min & x-max
        self.x_min_input.insert(10, self.x_min)
        self.x_max_input.insert(10, self.x_max)
        
        # show x-min & x-max input field
        self.x_min_input.grid(row=0, column=1, padx=5, pady=5)
        self.x_max_input.grid(row=2, column=1, padx=5, pady=5)
        
    def validate_x_min(self, x_min):
        '''
        Validating x-min ... 
        '''
        print(self.validate_x_min.__name__, self.validate_x_min.__doc__)
        
        # set x-min to 0.0 for empty input
        if not x_min: 
            self.x_min = 0.0
            return True
        
        try:
            self.x_min = float(x_min)
            return True
        except ValueError:
            return False
        
    def validate_x_max(self, x_max):
        '''
        Validating x-max ... 
        '''
        print(self.validate_x_max.__name__, self.validate_x_max.__doc__)
        
        # set x-max to 100.0 for empty input
        if not x_max: 
            self.x_max = 100.0
            return True
        
        try:
            self.x_max = float(x_max)
            return True
        except ValueError:
            return False

    def loaddata(self):
        '''
        loading directory chooser ...
        '''
        print(self.loaddata.__name__, self.loaddata.__doc__)
        
        directory = filedialog.askdirectory(title = "Select Directory")
        if directory: 
            try: 
                self.data = self.read_data(directory)
            except Exception as error: 
                print(error)
                messagebox.showerror("Failed!", "Failed to read '%s'"%directory)
        else:
            messagebox.showerror("Failed!", "Please choose a directory!!")
    
    def read_data(self, chosen_directory):
        '''
        Reading directory files ...
        '''
        print(self.read_data.__name__, self.read_data.__doc__)
        
        # list of files that are in the 'chosen_directory'
        files = []
        for (dirpath, dirnames, filenames) in walk(chosen_directory):
            files.extend(filenames)
            break
        # readable files those are with 'required_file_extension'
        required_file_extension = self.required_extension
        tuples = []
        for filename in files:
            file_name, file_extension = os.path.splitext(filename)
            if required_file_extension == file_extension:        
                is_corrupted = False
                temporary_tuples = []
                try:
                    # replace \ [backward slash] by / [forward slash]
                    #file_name_2 = r"{}".format(chosen_directory + '\\' + filename).replace("\\", '/')
                    file_name_2 = r"{}".format(chosen_directory + '/' + filename)
                    file = open(file_name_2, 'r')
                    lines = file.read().strip("\n").split("\n")
                    #index = 0
                    for line in lines: 
                        try:
                            # check whether the binding_energy is in the range of x-min & x-max
                            # if not in range then do not include into the list
                            binding_energy, intensity = line.split(' ')
                            binding_energy, intensity = float(binding_energy), float(intensity)
                            tuple = (float(binding_energy), float(intensity))
                            temporary_tuples.append(tuple)
                        except(ValueError):
                            is_corrupted = True
                            print("Broken file: ", filename)                        
                            break
                    file.close()
                except(FileNotFoundError):
                    pass
                if not is_corrupted:
                    for temporary_tuple in temporary_tuples:
                        tuples.append(temporary_tuple)
        return tuples
    
    def plotdata(self):
        '''
        Ploting data ...
        '''
        print(self.plotdata.__name__, self.plotdata.__doc__)
        
        if len(self.data) == 0:
            messagebox.showerror("Failed!", "No data loaded!!")
        else:
            # print([x for (x, y) in self.data])
            sorted(self.data)
            self.x_min, self.x_max = min(self.x_min, self.x_max), max(self.x_min, self.x_max)
            
            binding_energies = [b for (b, i) in self.data[0:500]]
            intensities = [0 for x in range(0, 500)]
            for x in range(0, len(self.data)):
                intensities[x % 500] += self.data[x][1]
                
            """
            x1, y1, x2, y2 = binding_energies[0], intensities[0], binding_energies[-1], intensities[-1]
            for x in range(0, len(intensities)):
                '''
                Assume, A(x1, y1) and B(x2, y2) forms straight line starting. Let P(x, y) is a point 
                on line AB and devide AB as ratio of AP:BP = m:n. So, 
                    x = (m*x2 + n*x1) / (m + n)
                    y = (m*y2 + n*y1) / (m + n)
                '''
                m, n = x + 1, 500 - (x + 1)
                y = (m*y2 + n*y1) / (m + n)
                intensities[x] -= intensities[x] - y
            """
            
            # check in range
            r_binding_energies = []
            r_intensities = []
            for x in range(0, len(binding_energies)):
                if binding_energies[x] >= self.x_min and binding_energies[x] <= self.x_max:
                    r_binding_energies.append(binding_energies[x])
                    r_intensities.append(intensities[x])
            binding_energies, intensities = r_binding_energies, r_intensities
            
            # window title    
            plt.figure('Binding energy (eV) VS Intensity (arbitrary units)')
            # figure title
            plt.title('Binding energy (eV) VS Intensity (arbitrary units)')
            plt.xlabel('Binding energy (eV)')
            plt.ylabel('Intensity (arbitrary units)')
            plt.plot(binding_energies, intensities)
            plt.show()
        
        
    def is_downward(self, x1, y1, x2, y2):
        try:
            slope = (y2 - y1) / (x2 - x1)
            if slope < 0:
                return True
            else: 
                return False
        except(ValueError, ZeroDivisionError):
            return False
        
    def calculate_area(self, x_coordinates, y_coordinates):
        '''
        calculate area of trapizoid
        '''
        return np.trapz(y_coordinates, x=x_coordinates)
        
   
   
if __name__ == "__main__":
    root = Tk()
    
    Spectroscopy(root)
    
    root.mainloop()