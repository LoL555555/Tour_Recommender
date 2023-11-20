import java.util.ArrayList; 
import java.util.Collections;

public class Tour {
    // Holds our tour of cities
    private ArrayList tour = new ArrayList(); // tour/ possible route is represented in array
    private double fitness = 0; // fitness of the route, the higher the better 
    private int distance = 0; // distance of the city
// Constructs a blank tour 
    public Tour(){
        for (int i = 0; i < TourManager.numberOfCities(); i++) { 
            tour.add(null);
    } }
    public Tour(ArrayList tour){ 
        this.tour = tour;
    }
// Creates a random individual (select any initial city) 
    public void generateIndividual() {
    // Loop through all our destination cities and add them into the pool
        for (int cityIndex = 0; cityIndex < TourManager.numberOfCities(); cityIndex++) {
            setCity(cityIndex, TourManager.getCity(cityIndex)); 
        }
        // Randomly reorder the tour (random selection)
        Collections.shuffle(tour); 
    }
// Gets a city from the tour
    public City getCity(int tourPosition) {
        return (City)tour.get(tourPosition); 
    }
// Sets a city in a certain position within a tour 
    public void setCity(int tourPosition, City city) {
        tour.set(tourPosition, city);
    // If the tours been altered we need to reset the fitness and distance fitness = 0;
        distance = 0;
    }
// Gets the tours fitness 
    public double getFitness() {
        if (fitness == 0) {
        fitness = 1/(double)getDistance();
        }
        return fitness; 
    }
// Gets the total distance of the tour 
    public int getDistance(){
        if (distance == 0) {
            int tourDistance = 0;
        // Loop through all possible cities in the routes
            for (int cityIndex=0; cityIndex < tourSize(); cityIndex++) {
            // Get last point of city where are travelling from
                City fromCity = getCity(cityIndex);
                // City we're travelling to
                City destinationCity;
                // Check if not last city last city, then set course to travel back to intial city 
                if(cityIndex+1 < tourSize()){
                destinationCity = getCity(cityIndex+1); }
                else{
                destinationCity = getCity(0);
                }
                // Get the distance between the two cities
                tourDistance += fromCity.distanceTo(destinationCity);
            }
            distance = tourDistance; 
            }
        return distance; }
    // Get number of cities on our tour 
    public int tourSize() {
    return tour.size(); 
    }
// Check if the tour contains a city
// Reconfirm to ensure that none of the city is missing (mutation probabilty) 
    public boolean containsCity(City city){
    return tour.contains(city); 
    }
    @Override
    public String toString() {
        String geneString = "|";
        for (int i = 0; i < tourSize(); i++) {
        geneString += getCity(i)+"|"; }
        return geneString; 
    }
}
