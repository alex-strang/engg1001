"""
Assignment 1
Semester 1, 2022
ENGG1001
"""


__author__ = "Alexander Strang, 47423510"
__email__ = "a.strang@uqconnect.edu.au"

HELP = """
    'i' - prompt for the input parameters
    'p <increments> <step>' - print out a table of distances to lift-off for different drag coefficients
    'h' - help message
    'q' - quit
"""


"""Task 1"""


def prompt_for_inputs():

    """
    prompt_for_inputs is a function that prompts the user for various
    inputs that will later be used in further calculations. The user is
    prompted for each input individualy, each inputs are then converted
    into a float for calculations.

    Parameters:
    m(float) = mass of plane (kg)
    ef(float) = engine force (N)
    ra(float) = reference area (m^2)
    ad(float) = air density (kg/mˆ3)
    vi(float) = intial velocity of airfract (m/s)
    vf(float) = velocity needed for takeoff (m/s)
    posi(float) = initial position of aircraft (m)
    ti(float) = time increments desired to calculations (s)
    drag_coeff(float) = the drag coefficent of the aircraft

    Return:
    values(tuple) = tuple of all values inputted, except drag coefficent
    drag_coeff(float) = drag coefficent entered 
    """
    
    m=float(input('Input mass of the plane (in kg): '))
    ef=float(input('Input engine force (in N): '))
    ra=float(input('Input reference area (in m^2): '))
    ad=float(input('Input air density (in kg/m^3): '))
    vi=float(input('Input initial velocity at start of runway (in m/s): '))
    vf=float(input('Input lift-off velocity (in m/s): '))
    posi=float(input('Input position of the start of the runway (in m): '))
    ti=float(input('Input time increment (in secs): '))
    drag_coeff=float(input('Input drag coefficient: '))
    values = (m, ef, ra, ad, vi, vf, posi, ti)
    return values, drag_coeff







"""Task 2"""

def compute_trajectory(values, drag_coeff):
    
    """
    compute_trajectory is a function designed to take the output of
    prompt_for_inputs (the values tuple and drag_coeff value, as inputs.
    Unpacking the values tuple so all values can be used in calculations
    and then use them to develop position and velocity vectors for each
    increment in time until take off velocity is reached.

    Parameters:
    values(tuple) = tuple of all values inputted (from task 1)
    drag_coeff(float) = drag coefficent entered (from task 1)

    Return:
    positions(tuple) =  tuple with position vectors at each increment in time 
    velocities(tuple) = tuple with velocity vectors at each increment in time

    """

    drag_coeff = drag_coeff
    m, ef, ra, ad, vi, vf, posi, ti = values
    v_new = 0
    v_old = vi
    velocities = ()
    p_new = 0
    p_old = posi
    positions = ()
    while v_old<vf:
        a=(1/m*(ef-(1/2*ad*(v_old**2)*ra*drag_coeff)))
        v_new=v_old+(a*ti)
        velocities += (round(v_new,3),)
        p_new = p_old + v_old*ti+(1/2*a*(ti)**2)
        positions += (round(p_new,3),)
        v_old = v_new
        p_old = p_new
         
    return positions, velocities

         




"""Task 3"""


def print_table(values, drag_coeff, increments, step):
    
    """
    print_table is a function designed to print a specifically laid out table
    of the maximum runway distance for a generic aircraft depending on the
    drag coefficent. It takes inputs from the prompt_for_info function and
    takes further inputs from the user regarding how many results and what
    variation is desired in the drag coefficents.

    Parameters:
    values(tuple) = tuple of all values inputted (from task 1)
    drag_coeff(float) = drag coefficent entered (from task 1)
    increments(int) = interger represenitng the number of increments calculated
    step(float) = a float of the difference between each drag coefficent

    Return:
    drag_tuple(tuple) = tuple with every drag coefficent tested
    runway_tuple(tuple) = tuple with every max runway distance found
    
    Prints table comparing both tuples
    """
    
    drag_count = 0
    runway_tuple = ()
    drag_tuple = ()
    while drag_count<increments:
        positions, velocities = compute_trajectory(values, drag_coeff)
        runway_tuple += (round(positions[-1],3),)
        drag_tuple += (round (drag_coeff,3),)
        drag_count += 1
        drag_coeff += step
    astrix_break = 38*'*'    
    print(astrix_break)
    print(f"*{'Drag coefficient' : ^18}*{'Runway distance' : ^17}*")
    print(astrix_break)
    for k in range(0, increments):
        print(f"*{drag_tuple[k] : ^18}*{runway_tuple[k] : ^17}*")
    print(astrix_break)
    





"""Task 4"""

def main():
    
    """
    the main function is a function of main code representing the user interface
    and the possible options avaliable for the user. It provides 4 option:
    the ability to start the prompt_for_inputs function (i), an input to quit
    the program (q), a list of commands for help (h), and a
    input that starts the print_table function

    Parameters:
    N/A

    Return:
    N/A

    """
    
    on = True
    values = None
    drag_coeff = None
    while on == True:
        option = input('Please enter a command: ')
        if option == 'i':
            values, drag_coeff = prompt_for_inputs()
        elif option =='h':
            print(HELP)
        elif option =='q':
            answer = input('Are you sure (y/n): ')
            if answer == 'y':
                on = False     
        elif "p" in option:
            if values == None:
                print('Please enter the parameters first.')
            else:
                option_split = option.split()
                increments = int(option_split[1])
                step = float(option_split[2])
                print_table(values, drag_coeff, increments, step)
                print("")

if __name__ == "__main__":
    main()



