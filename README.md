# LiFiReader
Inspired  by [LightByte](https://vgrserver.eecs.yorku.ca/~jenkin/papers/2018/icinco2018codd.pdf) by Robert Codd-Downey and Prof. Michael Jenkin.
## Iteration: 1
   ![LiFi](https://raw.githubusercontent.com/mahir1010/LiFiReader/SCRSHOT/LiFi%20OFF.png)
   Encodes only one byte of data. The green and white LEDs indicate most significant side and least significant side respectively. 
   The following image exhibits how the device will encode the character "M" (01001101).
   ![LiFi](https://raw.githubusercontent.com/mahir1010/LiFiReader/SCRSHOT/LiFi%20M.png)
   
### Algorithm
   1. Create a mask to extract Green and White Color (the activated LEDs will have a bright white color in the middle).
   2. Apply the masks to the image and find contours.
   3. By analyzing the coordinates of the contours detect the orientation of the device.
   4. Subtract the coordinates of boundary LEDs and calculate the scaled distance between two LEDs by (BOUNDARY_PIXEL_DISTANCE/BOUNDARY_ACTUAL_DISTANCE)*(CONSEQUTIVE_ACTUAL_DISTANCE)
   5. Refer to the white color contours as activated LEDs and calculate the difference between two consecutive activated LEDs. 
   6. Add "one" bit to the output. If the distance between two activated LEDs is x times more than the scaled distance, add x number of 'Zero' bit(s) to the output.
   7. Convert extracted bits to byte and show output.
   
#### Prototype : Iteration 1
   Breadboard Version:
   ![prototype](https://raw.githubusercontent.com/mahir1010/LiFiReader/SCRSHOT/LiFi.gif)

   
#### Future Development
    
   1. Print body for the first prototype.
      ![model](https://raw.githubusercontent.com/mahir1010/LiFiReader/SCRSHOT/3D%20Model.png)
   2. Change to narrow wavelength color to ensure optimal emmision under water.
   3. Use array of devices to send multiple bytes.
   4. Develop communication protcol similar to TCP, complete with two way handshaking and data stream.
