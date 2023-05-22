package speedControl;
public class speedControl {
    Variables variables = new Variables();

    // I see two methods. 
    
    public static void calculation(boolean objectExistence){
        if (objectExistence){

            boolean is_there = Variables.decodedData.is_there;
            double distance = Variables.decodedData.distance;
            double totalDistance = Variables.variables.totalDistance;
            double curve = Variables.variables.steepness;
            double allowedRange = Variables.variables.target;
            double decreasePower = 0.3; // by how much decrease power
            double inRangeSpeed = Variables.variables.inRangeSpeed;
            System.out.println("data incoming:" + distance);

            // double motorSpeed = distance > Math.abs(allowedRange) ? Math.pow(-((distance/i)-1),curve) + 1 : (distance == allowedRange ? 0 : allowedDistanceSpeed);
            double motorSpeed =  Math.pow(distance/totalDistance, 1/curve) * decreasePower;
            
            if(Math.abs(distance)<allowedRange){
                boolean push = is_there;
                motorSpeed *= inRangeSpeed;
            }
        }
    }
}
