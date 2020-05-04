## Advertisement insertion application

_Mechanism for ads insertion based on OpenCV package._

To insert ad you need to have the following:
- The logo to insert. Preferable formats are .png, .jpg;
- The video file for ad insertion.

The mechanism's main properties as follows:
- Detect stable contours in video using image threshold;
- Insert ad into detected contours.

To run the mechanism do the following:
- Download the repository with all consisting files;
- Install or upgrade necessary packages from requirements.txt;
- Run development server: ```python app.py``` and follow the link;
- Set preferable minimum time period for appearing unique logo in video. By default each logo will appear not less than 1.5 seconds. If you want to change time period click 'default', choose 'Put' method, click 'Try it out' and set parameter contour_threshold to the desired value;
- Set preferable minimum contour area for logo insertion. By default minimum contour area is 3000 pixels. If you want to change contour area click 'default', choose 'Put' method, click 'Try it out' and set parameter min_area_threshold to the desired value;
- If you want to check current model configuration, choose 'Get' method (Get current model configuration), and click 'Try it out'
- To insert advertisement into video choose 'POST' method, click 'Try it out', specify logo and video path and click 'Execute'. After the model performing you will get the link to download output video;
- If you want to check if the file is located on the server, choose 'Get' method (Get file by name), click 'Try it out' and specify filename.    