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

- From a terminal window type ```cd movie-ads-creator```. Then type ```bash execute.sh```. Wait till the installation will be completed;

- Find the **data** folder in **application**. The **data** folder is linked with the Docker container. It means the container has access to the files in this folder and the output video will be written into this folder. Copy video file and logo into **data** folder;

- All the required applications and frameworks are installed now. To begin working you need to start docker container. To do that type the next command: ```bash run.sh``` . The application is running, follow this link in browser: http://0.0.0.0:80/

- To begin working with application press '**default**'; 

- There is an opportunity to set preferable minimum time period for appearing unique logo in video. By default each logo will appear not less than 1.5 seconds. To change time period click '**Put**' method (Update model configuration), click '**Try it out**' and set parameter contour_threshold to the desired value, after that press '**Execute**';

- If you want to check current model configuration, choose '**Get**' method (Get current model configuration), and click '**Try it out**';

- To insert the ad into video choose '**POST**' method, click '**Try it out**', replace **'string'** in front of **'logo_path'** and **'video_path'** with the next paths: **/app/output/logo_name**, **/app/output/video_file_name**, where logo_name and video_file_name are the actual logo and video names from **data** folder. Click '**Execute**'. After execution you will see the model response "Video file has been processed.". If the model insert ads into the input video, the output video and report will appear in **data** folder;

- To handle new video \ logo just copy this video \ logo into the **data** folder and replace new video \ logo name with used one in 'logo_path' \ 'video_path';

- While you are working with the application, all the application logs are recorded in **log_file.log** that located in **data** folder. When you stop Docker container, the application will stop working and logs recording will be also stopped. So if you want to check application outputs while it is working just open **log_file.log** from your computer;

- To stop the application you need to stop the logs recording and Docker container. Press CTRL+С from the terminal window, then type the following: ```sudo docker container stop dock```;

- Every time when you want to use the application from the terminal window move to the **movie-ads-creator** folder and type ```bash run.sh```. Do not forget to follow this link after the application started: http://0.0.0.0:80/. To stop the application repeat the step below;

- The application runs unit tests every time when developer makes changes in code and commits them to the GitHub repository. This opportunity is realized with Git hooks. If you want to create Git hooks do the following:
- Create directory for scripts in Git repository: ```mkdir scripts```.
 - Use the editor to create scripts/run-test.bash file:
```shell script
#!/usr/bin/env bash

set -e

cd "${0%/*}/.."

# let's fake failing test for now 
echo "Running tests"
echo "............................" 
echo "Failed!" && exit 1
```
- Hook the script - create scripts/pre-commit.bash:
```shell script
#!/usr/bin/env bash

echo "Running pre-commit hook"
./scripts/run-tests.bash

# $? stores exit value of the last command
if [ $? -ne 0 ]; then
 echo "Tests must pass before commit!"
 exit 1
fi
```
- Install hooks with scripts/install-hooks.bash:
```shell script
#!/usr/bin/env bash

GIT_DIR=$(git rev-parse --git-dir)

echo "Installing hooks..."
# this command creates symlink to our pre-commit script
ln -s ../../scripts/pre-commit.bash $GIT_DIR/hooks/pre-commit
echo "Done!"
```
- Make all scripts executable with the following command: 
```chmod +x scripts/run-tests.bash scripts/pre-commit.bash scripts/install-hooks.bash ```
- Install the hook with the next command: ```./scripts/install-hooks.bash```.
Now, every time when you will try to create a commit, all tests must pass to allow that.


