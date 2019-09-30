<h1>Digital Control Systems Project 1</h1>

Full code and files can be found [here](https://github.com/DonStoddard5/ECE4422/tree/master/ece4422project1).

<h2>Wiring the system</h2>

In order to run the code, you must first wire up the hardware.

![Wiring diagram](/ece4422project1/readmeImages/WireDiagramProject1.jpg)

<h3>For the servo</h3>

**Black Wire:** goes to ground (pin 9)

**Red Wire:** goes to 3.3 volts (pin 1)

**White Wire:** goes to pin 11 (a.k.a. GPIO17

<h3>For the IMU</h3>

**Green Wire:** goes to 5 volts (pin 2)

**Blue Wire:** goes to ground (pin 6)

**Purple Wire:** goes to SCL (pin 5 a.k.a. GPIO3)

**Gray Wire:** goes to SDA (pin 3 a.k.a. GPIO2

For reference, here is a different picture of the Raspberry Pi I/O pins

![Raspberry Pi Diagram](/ece4422project1/readmeImages/raspberry_pi_circuit_note_fig2a.jpg)

<h2>Running the Code</h2>

<h3>basicIMU.py</h3>
You'll find the basicIMU.py file under: /ece4422project1/IMU-Servos/basicIMU.py

When you run it, you'll be prompted to enter an angle

![Input Prompt](/ece4422project1/readmeImages/basicIMU_firstInput.jpg)

This number (in degrees), will move the servo that far from where it currently is. If the input is positive, the servo will move clockwise. If it's negative, the servo will move counter-clockwise.

If the value is past the range of the servo, you'll get an error and will have to restart the program. This is a bug that needs to be fixed.

![Error Prompt](/ece4422project1/readmeImages/error.JPG)

<h3>fixedIMU.py</h3>
You'll find the fixedIMU.py file under: /ece4422project1/IMU-Servos/fixedIMU.py

When you run it, you'll be prompted to enter an angle

![Input Prompt](/ece4422project1/readmeImages/fixedIMU_firstInput.jpg)

This number (in degrees), will move the servo that far from where it currently is. If the input is positive, the servo will move clockwise. If it's negative, the servo will move counter-clockwise. From there, the program goes into a loop. The servo arm will move to stay in the same orientation as you physically rotate the servo around.

If the value is past the range of the servo, you'll get an error and will have to restart the program. This is a bug that needs to be fixed.

![Error Prompt](/ece4422project1/readmeImages/error.JPG)
