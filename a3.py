"""
Assignment 3
Semester 1, 2022
ENGG1001
"""

# NOTE: Do not import any other libraries!
import math
import numpy as np
import matplotlib.pyplot as plt

from numpy import ndarray


# Replace these <strings> with your name, student number and email address.
__author__ = "Alexander Strang,47423510"
__email__ = "<a.strang@uqconnect.edu.au>"


# Write your solution!

def nose_shape(x, L, Rb, d):
    """
    A function to calculate the corresponding y-position along the aircarft 
    given a certain x-position.
    
    Parameters
    ----------
    x (float): x-position along aircraft body
    L (float):  length of power-law body
    Rb (float): radius of base of power-law body
    d (float): exponent in power-law body

    Returns
    -------
    y (float): y-position along aircraft body

    """
    # formula to calculate y value
    y = Rb*((x/L)**d)
    return y


def plot_nose_shape(L, Rb, d, number_samples):
    """
    A function to plot the x-coordinates to thier corresponding y-coordinates
    found using nose_shape.

    Parameters
    ----------
    L (float):  length of power-law body
    Rb (float): radius of base of power-law body
    d (float): exponent in power-law body
    number_samples (int): number of points to be plotted 

    Returns
    -------
    None.

    """
    # initialise count, x-value and both lists used to plot
    n_count, x = 0, 0
    y_list, x_list = [], []
    
    # loop through and find each y-value and it's corresponding x-value 
    while n_count < number_samples:
        y_list.append(nose_shape(x, L, Rb, d))
        x_list.append(x)
        # update values
        x += L/(number_samples-1)
        n_count += 1

    # initialise plot, then plot data
    fig, ax = plt.subplots()
    ax.plot(x_list, y_list, marker='.')
    fig.suptitle(f'Power-law body: L={L}, Rb={Rb}, d={d}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid()
    plt.show()
    return None


def drag_coeff_panel(x0, y0, x1, y1):
    """
    A function to calculate a panels local drag coefficient given it's initial
    and final position

    Parameters
    ----------
    x0 (float): x-position of start position
    y0 (float): y-position of start position
    x1 (float): x-position of final position
    y1 (float): y-position of final position

    Returns
    -------
    c_d_panel (float): drag coefficient of local region

    """
    
    # find the angle between both points
    delta_x = x1-x0
    delta_y = y1-y0
    theta = math.atan((delta_y / delta_x))
    # formula for drag coefficient of panel
    c_d_panel = 2 * (math.sin(theta))**3
    return c_d_panel


def drag_coeff(L, Rb, d, number_panels):
    """
    A function to calculate the total drag coefficient of the nose-shape.

    Parameters
    ----------
    L (float):  length of power-law body
    Rb (float): radius of base of power-law body
    d (float): exponent in power-law body
    number_panels (int): number of panels to be used in calculations

    Returns
    -------
    Cd (float): Drag coefficient of entire nose 

    """
    
    # initialise all variables and counts used 
    y0, x0, x1, n_count, Cd, A = 0, 0, 0, 0, 0, 0
    # loop through each panel to find it's respective drag coefficient
    while n_count < number_panels:
        x1 += L/number_panels
        y1 = nose_shape(x1, L, Rb, d)
        c_d_p = drag_coeff_panel(x0, y0, x1, y1)
        dA = (((x1-x0)**2 + (y1-y0)**2)**0.5) * np.pi * (y0 + y1)   
        # redefine values for further calculations
        Cd += dA * c_d_p
        A += dA
        y0 = y1
        x0 = x1
        n_count += 1
    #apply formula for drag coefficient
    Cd = Cd/(A)
    return Cd


def print_table(L, Rb, number_panels, d_start, number_entries, step):
    """
    A function to generate a table of each power-law body exponent and the
    total drag coefficient of each respective exponent.

    Parameters
    ----------
    L (float):  length of power-law body
    Rb (float): radius of base of power-law body
    number_panels (int): number of panels to be used in calculations
    d_start (float): the initial exponent in power-law body
    number_entries (int): the number of entries to be put in the table
    step (float): the increment by which to increase the exponent by

    Returns
    -------
    None.

    """
    
    # initialise a count, define d and Cd_list and d_list used in the table
    d = d_start
    count = 0
    Cd_list, d_list = [], []
    # loop through to calculate the drag coefficient corresponding to each d 
    while count < number_entries:
        Cd = round(drag_coeff(L, Rb, d, number_panels), 4)
        Cd_list.append(Cd)
        d_list.append("{:.2f}".format(d))
        d += step
        count += 1
    # Format and print the table
    astrix_break = 29*'*'
    print(astrix_break)
    print(f"*{'d' : ^12}*{'C_D' : ^14}*")
    print(astrix_break)
    # loop through and print the data
    for k in range(0, number_entries):
        print(f"*{d_list[k] : ^12}*{Cd_list[k] : ^14}*")
    print(astrix_break)
    return None

class PowerLawBody(object):
    """
    A class to represent the Power law body.
    
    Attributes
    ----------
    L (float):  length of power-law body
    Rb (float): radius of base of power-law body
    d (float): exponent in power-law body
    number_panels (int): number of panels to be used in calculations

    Methods
    -------
    set_design_param(d):
        setter method to set the d value
    shape(x):
        calculates the y-position corresponding to a x-position
    drag_coeff():
        calculates the drag coefficent of a aircraft nose shape
    """

    def __init__(self, L, Rb, d, number_panels):
        """
        Constructs all the values needed to calculate drag coefficients.

        Parameters
        ----------
        L (float):  length of power-law body
        Rb (float): radius of base of power-law body
        d (float): exponent in power-law body
        number_panels (int): number of panels to be used in calculations
        number_panels : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        # construct and initialise all values needed for calculations
        self._L = L
        self._Rb = Rb
        self._d = d
        self._number_panels = number_panels
        return None
    
    def set_design_param(self, d):
        """
        Setter method used to activatevly change the value of d.
        Parameters
        ----------
        d (float): exponent in power-law body

        Returns
        -------
        None.

        """
        
        # re-initialise value of d 
        self._d = d
        return None
    
    def shape(self, x):
        """
        A method to calculate a points corresponding y-position given it's
        x-position.

        Parameters
        ----------
        x (float): x-position along aircraft body

        Returns
        -------
        y (float): y-position along aircraft body

        """
        
        # formula to calculate y-position given a x-position
        y = self._Rb*((x/self._L)**self._d)
        return y
    
    def drag_coeff(self):
        """
        A method to calculate the total drag coefficient of a nose shape
        
        Parameters
        ----------
        None
        
        Returns
        -------
        Cd (float): Drag coefficent of entire nose

        """
        # initialise all values used in calculations and the count
        y0, x0, x1, n_count, Cd, A = 0, 0, 0, 0, 0, 0
        # loop through to calculate the drag coefficent of each panel
        while n_count < self._number_panels:
            x1 += self._L/self._number_panels
            y1 = self.shape(x1)
            c_d_p = drag_coeff_panel(x0, y0, x1, y1)
            dA = (((x1-x0)**2 + (y1-y0)**2)**0.5) * np.pi * (y0 + y1)   
            # sum panel local drag coefficent and redefine values for loop
            Cd += dA * c_d_p
            A += dA
            y0 = y1
            x0 = x1
            n_count += 1

        # formula to calculate drag coefficent of entire nose shape
        Cd = Cd/(A)
        return Cd
    
    def __call__(self, d):
        """
        a method to allow the methods and class object to be callable as 
        functions.

        Parameters
        ----------
        d (float): exponent in power-law body

        Returns
        -------
        Callable drag_coeff() method

        """
        # reinitialise d value
        self._d = d
        return self.drag_coeff()
    
def plot_drag_coeff(nose_cap, d_start, d_stop, number_samples):
    """
    A function to plot the drag coefficent verses the corresponding exponent d.

    Parameters
    ----------
    nose_cap (PowerLawBody): the power-law body of interest
    d_start (float): the intial power-law body exponent for plotting
    d_stop (float): the final power-law body exponent for plotting
    number_samples (int): the number of samples to be plotted

    Returns
    -------
    None.

    """
    # initialise the d value, calculate the step increment, intiliase count
    # initiliase lists used in plotting
    d = d_start
    step = (d_stop - d_start)/(number_samples-1)
    count = 0
    Cd_list, d_list = [], []
    # loop through to find the drag coefficient corresponding to each d-value
    while count < number_samples:
        Cd = nose_cap.set_design_param(d)
        Cd = nose_cap.drag_coeff()
        # add the values to thier respective lists for plotting
        Cd_list.append(Cd)
        d_list.append(d)
        count += 1
        d += step
    # plot the function
    plt.plot(d_list, Cd_list, marker ='.')
    plt.title("Drag coefficients for power-law bodies")
    plt.xlabel('exponent, d')
    plt.ylabel('drag coefficient, C_D')
    plt.show()
    return None

def golden_section_search(f, a, b, tol):
    """
    A function to find the exponent that corresponds to the smallest 
    drag coefficient within a given interval range (a,b).
    
    Parameters
    ----------
    f : function in one variable, accepts and returns floats
    a (float): left end for initial search interval
    b (float): right end for initial search interval
    tol (float): tolerance threshold for stopping search

    Returns
    -------
    (float): exponent that corresponds to minimum drag coefficient

    """
    # initialise all values
    g = 0.618034
    dL = a
    dR = b
    # loop through until the search interval is smaller than the tolerance
    while tol < (dR - dL):
        dL = a + (1-g)*(b-a)
        dR = a+ g*(b-a)
        fR = f(dR)
        fL = f(dL)
        # check to see if interval bounds are in incorrect locations
        # adjust bounds accordingly 
        if fL < fR:
            b = dR 
            dR = dL
            fR = fL
            dL = a + (1-g)*(b-a)
            fL = f(dL)
        else: 
            a = dL
            dL = dR
            fL = fR
            dR = a + g*(b - a)
            fR = f(dR)
    # calculate the final estimation of the exponent
    return 0.5*(dL + dR)
            
    return
def main() -> None:
    """Entry point to interaction"""
    print("Implement your solution and run this file")


if __name__ == "__main__":
    main()
