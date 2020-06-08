using Microsoft.Quantum.Simulation.Core;
using Microsoft.Quantum.Simulation.Simulators;

namespace Quantum.QB4
{
    class Driver
    {
        static void Main(string[] args)
        {
            using (var sim = new QuantumSimulator())
            {
                
                var res = QB4Run.Run(sim).Result;
                var (p0000, p0001, p0010, p0011, p0100, p0101, p0110, p0111, 
                    p1000, p1001, p1010, p1011, p1100, p1101, p1110, p1111) = res;
                System.Console.WriteLine("0000 -> " + p0000 / 10000.0);
                System.Console.WriteLine("0001 -> " + p0001 / 10000.0);
                System.Console.WriteLine("0010 -> " + p0010 / 10000.0);
                System.Console.WriteLine("0011 -> " + p0011 / 10000.0);
                System.Console.WriteLine("0100 -> " + p0100 / 10000.0);
                System.Console.WriteLine("0101 -> " + p0101 / 10000.0);
                System.Console.WriteLine("0110 -> " + p0110 / 10000.0);
                System.Console.WriteLine("0111 -> " + p0111 / 10000.0);
                System.Console.WriteLine("1000 -> " + p1000 / 10000.0);
                System.Console.WriteLine("1001 -> " + p1001 / 10000.0);
                System.Console.WriteLine("1010 -> " + p1010 / 10000.0);
                System.Console.WriteLine("1011 -> " + p1011 / 10000.0);
                System.Console.WriteLine("1100 -> " + p1100 / 10000.0);
                System.Console.WriteLine("1101 -> " + p1101 / 10000.0);
                System.Console.WriteLine("1110 -> " + p1110 / 10000.0);
                System.Console.WriteLine("1111 -> " + p1111 / 10000.0);
            }
            
            System.Console.ReadKey();
        }
    }
}