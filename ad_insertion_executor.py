from models.opencv_model.ad_insertion import AdInsertion
import cv2 as cv
import numpy as np
import os


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
    return output


def ad_insertion_executor(video_path, logo, config):
    """
    Execute AdInsertion model for logo insertion
    :param video_path: video path
    :param logo: logo path
    :param config: config path
    :return: output video name
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
