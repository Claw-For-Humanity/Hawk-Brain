package speedControl;


public class Variables {
    
    public static class variables{
        static double totalDistance = 100;
        static double inRangeSpeed = 0.03;
        static double steepness = 4;
        static double target = Math.abs(4); // safe distance from target
    }

    public static class decodedData{
        static double distance = 0;
        static boolean is_there = false;
    }
}
