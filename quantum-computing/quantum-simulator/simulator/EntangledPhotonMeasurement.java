/* Simulator for Entangled Photon Measurements */
import java.lang.Math.*;
import java.math.BigDecimal;
import java.math.RoundingMode;
public class EntangledPhotonMeasurement 
{
    private String formatNumber(double value)
    {
        return new BigDecimal(value).setScale(2, RoundingMode.HALF_UP).toPlainString();
    }
    private double square(double value)
    {
        return value*value;
    }
    
    //State of the photons
    private double p00, p01, p10, p11;
    
    public EntangledPhotonMeasurement(double i00, double i01, double i10, double i11)
    {
        p00=i00; p01=i01; p10=i10; p11=i11;
        double check = p00*p00 + p01*p01 + p10*p10 + p11*p11;
        if(check>1.01 || check < 0.99)
            System.out.println("Error: Probabilities must add up to 1");
    }
    
    private void setIndependentPhotonAngles(double angle1, double angle2)
    {
        double r1 = Math.toRadians(angle1);
        double r2 = Math.toRadians(angle2);
        p00 = Math.cos(r1)*Math.cos(r2);
        p01 = Math.cos(r1)*Math.sin(r2);
        p10 = Math.sin(r1)*Math.cos(r2);
        p11 = Math.sin(r1)*Math.sin(r2);
    }
    
    private double m00, m01, m10, m11, m1angle, m2angle;
    public void setMeasurementAngles(double angle1, double angle2)
    {
        m1angle = angle1;
        m2angle = angle2;
        double r1 = Math.toRadians(angle1);
        double r2 = Math.toRadians(angle2);
        m00 = Math.cos(r1)*Math.cos(r2);
        m01 = Math.cos(r1)*Math.sin(r2);
        m10 = Math.sin(r1)*Math.cos(r2);
        m11 = Math.sin(r1)*Math.sin(r2);
    }
    
    public void reportMeasurementProbability()
    {
        //11
        double originalp1angle = m1angle;
        double originalp2angle = m2angle;
        double prob11 = square((p00*m00) + (p01*m01) + (p10*m10) + (p11*m11));
        //01
        setMeasurementAngles( 90 + originalp1angle, originalp2angle);
        double prob01 = square((p00*m00) + (p01*m01) + (p10*m10) + (p11*m11));
        //10
        setMeasurementAngles(originalp1angle, originalp2angle+90);
        double prob10 = square((p00*m00) + (p01*m01) + (p10*m10) + (p11*m11));
        //00
        setMeasurementAngles( 90 + originalp1angle, 90+ originalp2angle);
        double prob00 = square((p00*m00) + (p01*m01) + (p10*m10) + (p11*m11));
        //reset
        setMeasurementAngles(originalp1angle, originalp2angle);//reset to original
        
        System.out.println("Probability of 00 = "+formatNumber(prob00));
        System.out.println("Probability of 01 = "+formatNumber(prob01));
        System.out.println("Probability of 10 = "+formatNumber(prob10));
        System.out.println("Probability of 11 = "+formatNumber(prob11));

        System.out.println("Probability of Photon1 measured to be 1, given that Photon2 was measured to be 1 = "+formatNumber(prob11/(prob01+prob11)));
        System.out.println("Probability of Photon1 measured to be 1, given that Photon2 was measured to be 0 = "+formatNumber(prob10/(prob10+prob00)));
        System.out.println("Probability of Photon1 measured to be 0, given that Photon2 was measured to be 1 = "+formatNumber(prob01/(prob01+prob11)));
        System.out.println("Probability of Photon1 measured to be 0, given that Photon2 was measured to be 0 = "+formatNumber(prob00/(prob10+prob00)));

        System.out.println("Probability of Photon2 measured to be 1, given that Photon1 was measured to be 1 = "+formatNumber(prob11/(prob10+prob11)));
        System.out.println("Probability of Photon2 measured to be 1, given that Photon1 was measured to be 0 = "+formatNumber(prob01/(prob01+prob00)));
        System.out.println("Probability of Photon2 measured to be 0, given that Photon1 was measured to be 1 = "+formatNumber(prob10/(prob10+prob11)));
        System.out.println("Probability of Photon2 measured to be 0, given that Photon1 was measured to be 0 = "+formatNumber(prob00/(prob01+prob00)));
    }
    
    public void performMeasurement()
    {
        //11
        double originalp1angle = m1angle;
        double originalp2angle = m2angle;
        double prob11 = square((p00*m00) + (p01*m01) + (p10*m10) + (p11*m11));
        setMeasurementAngles( 90 + originalp1angle, originalp2angle);//01
        double prob01 = square((p00*m00) + (p01*m01) + (p10*m10) + (p11*m11));
        setMeasurementAngles(originalp1angle, originalp2angle+90);//10
        double prob10 = square((p00*m00) + (p01*m01) + (p10*m10) + (p11*m11));
        setMeasurementAngles( 90 + originalp1angle, 90+ originalp2angle);//00
        double prob00 = square((p00*m00) + (p01*m01) + (p10*m10) + (p11*m11));
        //reset
        setMeasurementAngles(originalp1angle, originalp2angle);//reset to original
        
        double rand = Math.random();
        if(rand<prob00)
        {
            //Measured to be 00
            double angle1 = m1angle+90;//Add 90 for anti-alignment. 0 means anti-alignment
            double angle2 = m2angle+90;//Add 90 for anti-alignment. 0 means anti-alignment
            setIndependentPhotonAngles(angle1, angle2);
            System.out.println("-------------------------------------------------------");
            System.out.println("Measured 00");
            System.out.println("After measurement, the photon angles are "+formatNumber(angle1)+" and "+formatNumber(angle2));
        }
        else if(rand<prob00+prob01)
        {
            //Measured to be 01
            double angle1 = m1angle+90;//Add 90 for anti-alignment. 0 means anti-alignment
            double angle2 = m2angle;//1 means alignment. Don't add 90
            setIndependentPhotonAngles(angle1, angle2);
            System.out.println("-------------------------------------------------------");
            System.out.println("Measured 01");
            System.out.println("After measurement, the photon angles are "+formatNumber(angle1)+" and "+formatNumber(angle2));
        }
        else if(rand<prob00+prob01+prob10)
        {
            //Measured to be 10
            double angle1 = m1angle;//1 means alignment. Don't add 90
            double angle2 = m2angle+90;//Add 90 for anti-alignment. 0 means anti-alignment
            setIndependentPhotonAngles(angle1, angle2);
            System.out.println("-------------------------------------------------------");
            System.out.println("Measured 10");
            System.out.println("After measurement, the photon angles are "+formatNumber(angle1)+" and "+formatNumber(angle2));
        }
        else
        {
            //Measured to be 11
            double angle1 = m1angle;//1 means alignment. Don't add 90
            double angle2 = m2angle;//1 means alignment. Don't add 90
            setIndependentPhotonAngles(angle1, angle2);
            System.out.println("-------------------------------------------------------");
            System.out.println("Measured 11");
            System.out.println("After measurement, the photon angles are "+formatNumber(angle1)+" and "+formatNumber(angle2));
        }
    }
    
    
    public static void main(String[] args)
    {
        //Compute probabilities. But we don't make any measurement. So the Photon state is not changed.
        EntangledPhotonMeasurement pairPrediction = new EntangledPhotonMeasurement(0.707106, 0, 0, 0.707106);
        pairPrediction.setMeasurementAngles(45,45);
        pairPrediction.reportMeasurementProbability();
        
        //Perform some measurements. Measurements will change the photon states.
        for(int i=0;i<10;i++)
        {
            EntangledPhotonMeasurement pairExperiment = new EntangledPhotonMeasurement(0.707106, 0, 0, 0.707106);
            pairExperiment.setMeasurementAngles(45,45);
            pairExperiment.performMeasurement();
        }
    }
}
