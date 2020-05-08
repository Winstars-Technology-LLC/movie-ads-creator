from models.opencv_model.ad_insertion import AdInsertion
import cv2 as cv
import numpy as np
import os
from pathlib import Path


def add_audio(video_path):
    """
    Extract audio file from input video and add it to output video
    :param video_path: video path
    :return: output video name
    """
    input_video_name = video_path.split('/')[-1].split('.')[0]
    idx = np.random.randint(0, 10000)
    audio_name = 'audio_{}_{}.aac'.format(input_video_name, idx)
    os.system('ffmpeg -i {} -vn -acodec copy files/{}'.format(video_path, audio_name))
    output = 'output_{}_{}.avi'.format(input_video_name, idx)
    os.system('ffmpeg -i files/result.avi -i files/{} -codec copy -shortest {}'.format(audio_name, output))


def ad_insertion_executor(video_path, logo, config):
    """
    Execute AdInsertion model for logo insertion
    :param video_path: video path
    :param logo: logo path
    :param config: config path
    :return: output video name
    """
    files_path = str(Path.cwd()) + '/files'
    Path(files_path).mkdir(parents=True, exist_ok=True)
    capture = cv.VideoCapture(video_path)

    if int(capture.get(cv.CAP_PROP_FPS)) == 0 or cv.imread(logo) is None:
        message = 'ERROR WHILE ENTERING LOGO OR VIDEO PATH.'
        print(message)
    else:
        frame_width = int(capture.get(3))
        frame_height = int(capture.get(4))
        four_cc = cv.VideoWriter_fourcc(*'FMP4')  # XVID FMP4 X264
        frames_count = int(capture.get(cv.CAP_PROP_FRAME_COUNT))
        fps = capture.get(cv.CAP_PROP_FPS)
        out_name = 'files/result.avi'
        out = cv.VideoWriter(out_name, four_cc, fps, (frame_width, frame_height), True)

        # Preprocessing
        print('Preprocessing is running...')
        data = []
        for i in range(frames_count):
            ret, frame = capture.read()
            if ret:
                ad_insertion = AdInsertion(frame, logo, i, data, None)
                ad_insertion.build_model(config)
                ad_insertion.data_preprocessed()
            else:
                break
        data = np.array(data)
        np.save('files/data.npy', data)
        capture.release()
        print('Preprocessing completed.')

        # Detection
        print('Detection is running...')
        ad_insertion = AdInsertion(None, None, None, None, fps)
        ad_insertion.build_model(config)
        ad_insertion.detect_surfaces()
        stable_contours = ad_insertion.stable_contours
        print('Detection completed.')

        # Ads insertion
        if len(stable_contours) != 0:
            print('Insertion is running...')
            capture = cv.VideoCapture(video_path)
            for i in range(frames_count):
                ret, frame = capture.read()
                if ret:
                    if i in stable_contours[:, 0]:
                        ad_insertion = AdInsertion(frame, logo, i, None, None)
                        ad_insertion.build_model(config)
                        ad_insertion.insert_ad(stable_contours)
                    out.write(frame)
                else:
                    break
            add_audio(video_path)
            print('Insertion completed.')
        else:
            message = 'STABLE CONTOURS WITH SPECIFIED TIME PERIOD WERE NOT FOUND.'
            print(message)

        capture.release()
        out.release()
        message = 'Video file has been processed.'
        print(message)

    for filename in os.listdir(files_path):
        file_path = os.path.join(files_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return message

