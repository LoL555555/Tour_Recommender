import java.util.Collections;
import java.util.ArrayList; 
public class TourManager {
    static ArrayList<City> cities = new ArrayList<>();
    public void addCity(City c) {
        cities.add(c);
    }
    public static int numberOfCities() {
        return cities.size();
    }
    public static City getCity(int index) {
        return cities.get(index);
    }

}
