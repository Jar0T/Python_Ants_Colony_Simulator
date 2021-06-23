from Simulation import Simulation

def main():
    sim = Simulation(300, 300)
    sim.play()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()