/* Simulator for Photon Qubit Measurements */
import java.lang.Math.*;
public class PhotonPolarizationMeasurement 
{
    private double polarizationAngle;

    public PhotonPolarizationMeasurement(double angle) 
    {
        polarizationAngle = angle;
    }
    
    //Measurement returns boolean true for "aligned" and false for "anti-aligned"
    //Qubit value 1 = Aligned (true)
    //Qubit value 0 = Anti-Aligned (false)
    //Observe how measurement causes the state to change
    public boolean measurePolarization(double angle)
    {
        double diffAngle = angle-polarizationAngle;
        double cosDiffAngle = Math.cos(Math.toRadians(diffAngle));
        double probabilityAlign = cosDiffAngle*cosDiffAngle;
        double probabilityAntiAlign = 1 - probabilityAlign;
        
        if(Math.random()<probabilityAlign)
        {
            polarizationAngle = angle;
            return true; //TRUE means "Aligned"
        }
        else
        {
            polarizationAngle = angle+90;
            return false; //FALSE means "Anti-Aligned"
        }
    }
    
    public static void main(String[] args)
    {
        //Experiment 1
        // PhotonPolarizationMeasurement photon = new PhotonPolarizationMeasurement(90);
        // for(int i=0;i<5;i++)System.out.println(photon.measurePolarization(45));
        
        //Experiment 2
        int trueCount = 0; 
        int falseCount = 0;
        for(int i=0;i<1000;i++)
        {
            PhotonPolarizationMeasurement photon = new PhotonPolarizationMeasurement(0);
            if(photon.measurePolarization(20))
            {
                trueCount++;
            }
            else
            {
                falseCount++;
            }
        }
        //Mapping: TRUE to 1, and FALSE to 0
        double mean = (1.0*trueCount + 0*falseCount)/(trueCount+falseCount);
        double variance = ((1.0-mean)*(1.0-mean)*trueCount + mean*mean*falseCount)/(trueCount+falseCount);
        double SD = Math.sqrt(variance);
        System.out.println("MEAN: "+mean+"\r\nStandard Deviation: "+SD);
    }
}
