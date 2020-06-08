namespace Quantum.QB4
{
    open Microsoft.Quantum.Primitive;
    open Microsoft.Quantum.Canon;

	operation QB4Run () : (Int,Int,Int,Int,Int,Int,Int,Int,Int,Int,Int,Int,Int,Int,Int,Int)
    {
        body
        {
			mutable num0000 = 0;
			mutable num0001 = 0;
			mutable num0010 = 0;
			mutable num0011 = 0;
			mutable num0100 = 0;
			mutable num0101 = 0;
			mutable num0110 = 0;
			mutable num0111 = 0;
			mutable num1000 = 0;
			mutable num1001 = 0;
			mutable num1010 = 0;
			mutable num1011 = 0;
			mutable num1100 = 0;
			mutable num1101 = 0;
			mutable num1110 = 0;
			mutable num1111 = 0;

            using (qubits = Qubit[4])
            {
                for (test in 1..10000)
                {
                    Set (Zero, qubits[0]);
                    Set (Zero, qubits[1]);
					Set (Zero, qubits[2]);
					Set (Zero, qubits[3]);

					//Demo of pass through (NOP)
					// Set (Zero, qubits[0]);
                    // Set (One, qubits[1]);
					// Set (One, qubits[2]);
					// Set (Zero, qubits[3]);

					//Demo of NOT gate
					// Set (Zero, qubits[0]);
					// X(qubits[0]);

					//Demo of Hadamard
					// Set (Zero, qubits[0]);
					// H(qubits[0]);

					//Demo of SWAP
					//Set (One, qubits[0]);
					//SWAP (qubits[0],qubits[1]);

					//Demo of Controlled-NOT   ( CNOT )
					//Set (One, qubits[0]);
                    //Set (Zero, qubits[1]);
                    //CNOT(qubits[0],qubits[1]);

					//Demo of Bell State
					//Set (Zero, qubits[0]);
                    //Set (Zero, qubits[1]);
                    //H(qubits[0]);
                    //CNOT(qubits[0],qubits[1]);

					//Demo of Toffoli Gate in general configuration
					//Set (One, qubits[0]);
                    //Set (One, qubits[1]);
					//Set (One, qubits[2]);
					//CCNOT(qubits[0],qubits[1],qubits[2]);

					//Demo of Toffoli Gate in NOT configuration
					//Set (One, qubits[0]); // Always 1
                    //Set (One, qubits[1]); // Always 1
					//Set (One, qubits[2]); // Input of NOT gate. Gets inverted by NOT
					//CCNOT(qubits[0],qubits[1],qubits[2]);

					//Demo of Toffoli Gate in AND configuration
					//Set (One, qubits[0]); // Input 1 of AND
                    //Set (One, qubits[1]); // Input 2 of AND
					//Set (Zero, qubits[2]);// Initialized to 0. Gets the result of AND
					//CCNOT(qubits[0],qubits[1],qubits[2]);

					//Demo of Toffoli Gate in FANOUT configuration
					//Set (One, qubits[0]); // Always 1
                    //Set (One, qubits[1]); // Input & Pass through.
					//Set (Zero, qubits[2]); //Initialized to 0. Gets a result of the fanout from qubits[1]
					//CCNOT(qubits[0],qubits[1],qubits[2]);

					
					
					
                    let res0 = M (qubits[0]);
					let res1 = M (qubits[1]);
					let res2 = M (qubits[2]);
					let res3 = M (qubits[3]);

					if(res3 == Zero && res2 == Zero && res1 == Zero && res0 == Zero){set num0000 = num0000 + 1;}
					if(res3 == Zero && res2 == Zero && res1 == Zero && res0 == One ){set num0001 = num0001 + 1;}
					if(res3 == Zero && res2 == Zero && res1 == One  && res0 == Zero){set num0010 = num0010 + 1;}
					if(res3 == Zero && res2 == Zero && res1 == One  && res0 == One ){set num0011 = num0011 + 1;}
					if(res3 == Zero && res2 == One  && res1 == Zero && res0 == Zero){set num0100 = num0100 + 1;}
					if(res3 == Zero && res2 == One  && res1 == Zero && res0 == One ){set num0101 = num0101 + 1;}
					if(res3 == Zero && res2 == One  && res1 == One  && res0 == Zero){set num0110 = num0110 + 1;}
					if(res3 == Zero && res2 == One  && res1 == One  && res0 == One ){set num0111 = num0111 + 1;}
					if(res3 == One  && res2 == Zero && res1 == Zero && res0 == Zero){set num1000 = num1000 + 1;}
					if(res3 == One  && res2 == Zero && res1 == Zero && res0 == One ){set num1001 = num1001 + 1;}
					if(res3 == One  && res2 == Zero && res1 == One  && res0 == Zero){set num1010 = num1010 + 1;}
					if(res3 == One  && res2 == Zero && res1 == One  && res0 == One ){set num1011 = num1011 + 1;}
					if(res3 == One  && res2 == One  && res1 == Zero && res0 == Zero){set num1100 = num1100 + 1;}
					if(res3 == One  && res2 == One  && res1 == Zero && res0 == One ){set num1101 = num1101 + 1;}
					if(res3 == One  && res2 == One  && res1 == One  && res0 == Zero){set num1110 = num1110 + 1;}
					if(res3 == One  && res2 == One  && res1 == One  && res0 == One ){set num1111 = num1111 + 1;}
					
					
                }
                Set(Zero, qubits[0]);
				Set(Zero, qubits[1]);
				Set(Zero, qubits[2]);
				Set(Zero, qubits[3]);
            }
            

            return (num0000, num0001, num0010, num0011, num0100, num0101, num0110, num0111, 
					num1000, num1001, num1010, num1011, num1100, num1101, num1110, num1111);

        }
    }

	operation Set (desired: Result, q1: Qubit) : ()
    {
        body
        {
            let current = M(q1);
            if (desired != current)
            {
                X(q1);
            }
        }
    }

}
