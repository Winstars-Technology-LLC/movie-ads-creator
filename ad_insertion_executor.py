from models.opencv_model.ad_insertion import AdInsertion
import cv2 as cv
import time
import numpy as np
import os
import ffmpeg


def add_audio(video_path):
    os.system('ffmpeg -i {} -vn -acodec copy files/output-audio.aac'.format(video_path))
    output = 'output.avi'
    os.system('ffmpeg -i files/result.avi -i files/output-audio.aac -codec copy -shortest {}'.format(output))
    return output


def ad_insertion_executor(video_path, logo, config):
    """
    Execute AdInsertion model for logo insertion
    :param video_path: video path
    :param logo: logo path
    :param config: config path
    :return:
    """
    capture = cv.VideoCapture(video_path)
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
        _, frame = capture.read()
        ad_insertion = AdInsertion(frame, logo, i, data, None)
        ad_insertion.build_model(config)
        ad_insertion.data_preprocessed()
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
    print('Insertion is running...')
    capture = cv.VideoCapture(video_path)
    for i in range(frames_count):
        _, frame = capture.read()
        if i in stable_contours[:, 0]:
            ad_insertion = AdInsertion(frame, logo, i, None, None)
            ad_insertion.build_model(config)
            ad_insertion.insert_ad(stable_contours)
        out.write(frame)
    output = add_audio(video_path)
    print('Insertion completed.')

    capture.release()
    out.release()
    return output


'''
film_path = 'SET FILM NAME'
logo_path = 'SET LOGO NAME'
config_path = 'models/configurations/configurations.yml'

ad_insertion_executor(film_path, logo_path, config_path, report)
'''
