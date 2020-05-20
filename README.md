## Advertisement insertion application

_Mechanism for ads insertion based on OpenCV package._

To insert ads you need to have the following:
- The logo to insert. **Preferable formats are .png, .jpg**;
- The video file for ad insertion;

The mechanism's main properties as follows:
- Detect stable contours in video using image threshold;
- Find stable contours among existing;
- Insert ad into detected contours;
- Extract audio track from input video and add it to the output.

To run the mechanism do the following:
- **Create a folder** for the application:
1. From a terminal window, change to the local directory where you want to place the application.
2. Type the following command: ```mkdir application```.
3. Move to the created folder: ```cd application```.

- Download the repository with all consisting files:
1. From the repository, select **Clone or download**.
2. Copy the repository URL.
3. From a terminal window write the command: ```git clone <URL>```, where URl is a copied repository URL.

- From a terminal window type ```cd movie-ads-creator```. Then type ```bash execute.sh```. Wait till the installation will be completed.
- Now the **data** folder is linked with the Docker container. It means the container has access to the files in this folder and the output video will be written into this folder;

- To begin working with application press '**default**'; 

- There is an opportunity to set preferable minimum time period for appearing unique logo in video. By default each logo will appear not less than 1.5 seconds. To change time period click '**Put**' method (Update model configuration), click '**Try it out**' and set parameter contour_threshold to the desired value, after that press '**Execute**';

- If you want to check current model configuration, choose '**Get**' method (Get current model configuration), and click '**Try it out**';

- To insert the ad into video choose '**POST**' method, click '**Try it out**', replace **'string'** in front of **'logo_path'** and **'video_path'** with the next paths: **/app/output/logo_name**, **/app/output/video_file_name**, where logo_name and video_file_name are the actual logo and video names from **data** folder. Click '**Execute**'. After execution you will see the model response "Video file has been processed.". If the model insert ads into the input video, the output video and report will appear in **data** folder;

- To handle new video \ logo just copy this video \ logo into the **data** folder and replace new video \ logo name with used one in 'logo_path' \ 'video_path';


- To stop the application press CTRL+С from the terminal window.     