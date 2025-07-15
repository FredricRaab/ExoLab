The [Magnitude.io](https://magnitude.io) ExoLab is a STEM education program that connects students with experiments aboard the International Space Station (ISS) by providing a hands-on, project-based learning experience where students can conduct plant biology experiments in a specialized growth chamber, the ExoLab, and compare their results with a similar experiment happening on the ISS. This allows students to investigate how microgravity affects plant growth and other biological processes. 

At the 2024 Space Exploration Educators Conference at [Space Center Houston](https://spacecenter.org/), Magnitude.io’s founder, Ted Tagami, challenged makers to create an open-source version of their ExoLab.

This project replicates the Magnitude.io ExoLab as closely as possible in size and functionality and seamlessly interfaces to their web-based application.  It was successfully used on their 11th mission to the ISS in the Fall of 2024.

The ExoLab growth chamber contains a programmable 64 element LED array for lighting, sensors for measuring temperature, humidity, carbon dioxide, and light intensity, as well as a camera that periodically takes pictures of the seedlings growth over the course of the experiment. Using a Magnitude.io’s web-based application, images from this camera and the data from these measurements are then shown together. Students can compare the information from their lab to other labs all over the world, as well as the microgravity experiment that’s simultaneously happening on the ISS.

The original ExoLab enclosure is based on the [standard CubeLab platform](https://spacetango.com/spaceservices/] for experimentation on the ISS and measures 10cm x 10cm x20cm, also known as 2U.  This implementation adds an additional 1U to the base of the enclosure for the Raspberry Pi 3B+. The enclosure has also been modified to make it easy to 3D print and assemble. The original Exolab’s difficult-to-fabricate U-shaped clear acrylic cover has been replaced by a single slide-in clear cover.  

While the software implementation enables interfacing to the Magnitude.io network which requires a license, it can also be used standalone.  Configuration parameters for lighting and timings are stored on the SD card in an editable JSON file, data measurements in a CSV file, and JPG images in a folder. 



Additionally, this implementation enables use of [Adafruit.io](https://io.adafruit.com/), a web-based platform for storing and visualizing data from Adafruit.com.  The current implementation fits within the limits of the  free version, but could be extended to enable more command and control functions with the paid version (currently $99 per year).

Software is coded in Python with the appropriate Adafruit and Raspberry libraries.  Magnitude.io’s servers do not store the JPG images, just the URL to this image.  In this implementation, images are stored on [Amazon Web Services (S3)](https://aws.amazon.com/s3/) using a free account.
