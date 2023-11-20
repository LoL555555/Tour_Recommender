public class Population {
    // Holds population of tours 
    Tour[] tours;
    // Construct a population
    public Population(int populationSize, boolean initialise) {
        tours = new Tour[populationSize];
        // If we need to initialise a population of tours do so 
        if (initialise) {
        // Loop and create offspring route
            for (int i = 0; i < populationSize(); i++) {
                Tour newTour = new Tour(); 
                newTour.generateIndividual(); 
                saveTour(i, newTour);
            }
        }
    }
        
        // Saves generated offspring route
    public void saveTour(int index, Tour tour) {
        tours[index] = tour; 
    }
        // Gets a route from population 
    public Tour getTour(int index) {
        return tours[index]; 
    }
    // Gets the best route in the population 
    public Tour getFittest() {
        Tour fittest = tours[0];
        // Loop through cities to find fittest
        for (int i = 1; i < populationSize(); i++) {
            if (fittest.getFitness() <= getTour(i).getFitness()) { 
                fittest = getTour(i);
            } 
        }
        return fittest; 
    }
        // Gets population size 
    public int populationSize() {
        return tours.length;
    }
}
