## Advertisement insertion application

_Mechanism for ads insertion based on OpenCV package._

To insert ad you need to have the following:
- The logo to insert. Preferable formats are .png, .jpg;
- The video file for ad insertion;
- Python 3.7 to be installed.

The mechanism's main properties as follows:
- Detect stable contours in video using image threshold;
- Insert ad into detected contours.

To run the mechanism do the following:
- Download the repository with all consisting files:
1. From the repository, select **Clone or download**.
2. Copy the repository URL.
3. From a terminal window, change to the local directory where you want to clone your repository.
4. Write the command: ```git clone <URL>```, where <URl> is copied repository URL;
- Create project virtual environment: 
1. From the terminal move to the downloaded repository and install virtualenv package:  ```pip install virtualenv```.
2. To create virtual environment specify a path. In the local directory type the following: ```virtualenv my_venv```.
3. Activate the virtual environment by the following command: ```source my_venv/bin/activate```. 
- Install or upgrade necessary packages from requirements.txt - from the terminal window move to the downloaded repository and write ```pip install -r requirements.txt```;
- Install FFmpeg tool:
1. Update the packages list: ```$ sudo apt update```.
2. Install FFmpeg by typing the following command: ```$ sudo apt install ffmpeg```.
- Run development server: from the terminal window type: ```python app.py``` and follow the link below;
- To begin working with application press '**default**'; 
- If you want, you may set preferable minimum time period for appearing unique logo in video. By default each logo will appear not less than 1.5 seconds. To change time period click 'Put' method (Update model configuration), click 'Try it out' and set parameter contour_threshold to the desired value, after that press '**Execute**';
- If you want , you may set preferable minimum contour area for logo insertion. By default minimum contour area is 3000 pixels. To change contour area, click 'Put' method (Update model configuration), click 'Try it out' and set parameter min_area_threshold to the desired value, after that press '**Execute**';
- If you want to check current model configuration, choose 'Get' method (Get current model configuration), and click 'Try it out'
- To insert advertisement into video choose 'POST' method, click 'Try it out', specify logo and video path and click 'Execute'. After the model performing you will get the link to download output video;
- If you want to check if the file is located on the server, choose 'Get' method (Get file by name), click 'Try it out' and specify filename;
- To stop the application press CTRL+c from the terminal window.     