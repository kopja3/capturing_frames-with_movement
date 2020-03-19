# capturing_frames-with_movement
For complete machine vision system is needed to have Raspberry Pi (most likely ver. 4) along with rest project files:

Project structure:
|--config
|  |-- gmg.json	
|  |-- mog.json
|-- output_gmg
|  |-- 20181014-143423.jpg
|  |-- ...
|-- output_mog
|  |-- 20200318-104253.jpg
|  |-- ...
|-- pyimadesearch  
|  |-- utils
|  |  |--_init_.py
|  |  |-- conf.py
|  |--__init_.py
|  |-- keyclipwriter.py

Machine vision application that captures motion picture frames in the video stream. The operation is based on buffering the frames so
that the frames are recorded before and after the movement. When motion is detected, any frames can be saved from the buffer to the disk.
Until no further motion is detected. Application use background subtraction and contour processing. 

Analyzing video (birds_10min.mp4):
(py3cv4) pi@raspberrypi:~/HobbyistBundle_Code/chapter09-bird_feeder_monitor $ python bird_mon.py --conf config/mog.json --video birds_10min.mp4

Analyzing cameras video stream:
(py3cv4) pi@raspberrypi:~/HobbyistBundle_Code/chapter09-bird_feeder_monitor $ python bird_mon.py --conf config/mog.json 
