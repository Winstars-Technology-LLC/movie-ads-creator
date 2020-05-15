from models.opencv_model.ad_insertion import AdInsertion
import cv2 as cv
import numpy as np
import os
from pathlib import Path


def add_audio(video_path, filename):
    """
    Extract audio file from input video and add it to output video
    :param video_path: video path
    :param filename: filename
    :return: output video name
    """
    idx = np.random.randint(0, 10000)
    audio_name = 'audio_{}_{}.aac'.format(filename, idx)
    os.system('ffmpeg -i {} -vn -acodec copy files/{}'.format(video_path, audio_name))
    output = 'output/output_{}_{}.avi'.format(filename, idx)
    os.system('ffmpeg -i files/result.avi -i files/{} -codec copy -shortest {}'.format(audio_name, output))


def preprocessing(frames_count, capture, logo, video_info, config):
    """
    Model preprocessing
    :param frames_count: video frames count
    :param capture: video object
    :param logo: logo path
    :param video_info: video info
    :param config: config path
    :return:
    """
    print('Preprocessing is running...')
    data = []
    for i in range(frames_count):
        ret, frame = capture.read()
        if ret:
            ad_insertion = AdInsertion(frame, logo, i, data, video_info)
            ad_insertion.build_model(config)
            ad_insertion.data_preprocessed()
        else:
            break
    data = np.array(data)
    np.save('files/data.npy', data)
    capture.release()
    print('Preprocessing completed.')


def detection(video_info, config):
    """
    Model detection method
    :param video_info: video info
    :param config: config path
    :return: stable contours
    """
    print('Detection is running...')
    ad_insertion = AdInsertion(None, None, None, None, video_info)
    ad_insertion.build_model(config)
    ad_insertion.detect_surfaces()
    stable_contours = ad_insertion.stable_contours
    print('Detection completed.')
    return stable_contours


def insertion(video_path, frames_count, logo, video_info,
              config, stable_contours, out, input_video_name):
    """
    Model insertion method
    :param video_path: video path
    :param frames_count: video frames count
    :param logo: logo path
    :param video_info: video info
    :param config: config path
    :param stable_contours: stable contours
    :param out: video writer object
    :param input_video_name: input video name
    :return: message that describes insertion result
    """
    if len(stable_contours) != 0:
        print('Insertion is running...')
        capture = cv.VideoCapture(video_path)
        for i in range(frames_count):
            ret, frame = capture.read()
            if ret:
                if i in stable_contours[:, 0]:
                    ad_insertion = AdInsertion(frame, logo, i, None, video_info)
                    ad_insertion.build_model(config)
                    ad_insertion.insert_ad(stable_contours)
                out.write(frame)
            else:
                break
        add_audio(video_path, input_video_name)
        capture.release()
        out.release()
        print('Insertion completed.')
    else:
        message = 'STABLE CONTOURS WITH SPECIFIED TIME PERIOD WERE NOT FOUND.'
        print(message)

    message = 'Video file has been processed.'
    print(message)
    return message


def ad_insertion_executor(video_path, logo, config):
    """
    Execute AdInsertion model for logo insertion
    :param video_path: video path
    :param logo: logo path
    :param config: config path
    :return: message that describes insertion result
    """
    input_video_name = video_path.split('/')[-1].split('.')[0]
    files_path = str(Path.cwd()) + '/files'
    output_path = str(Path.cwd()) + '/output'
    Path(files_path).mkdir(parents=True, exist_ok=True)
    Path(output_path).mkdir(parents=True, exist_ok=True)
    capture = cv.VideoCapture(video_path)

    if int(capture.get(cv.CAP_PROP_FPS)) == 0 or cv.imread(logo) is None:
        message = 'ERROR WHILE ENTERING LOGO OR VIDEO PATH.'
        print(message)
    else:
        frame_width = int(capture.get(3))
        frame_height = int(capture.get(4))
        frame_square = frame_height * frame_width
        four_cc = cv.VideoWriter_fourcc(*'FMP4')  # XVID FMP4 X264
        frames_count = int(capture.get(cv.CAP_PROP_FRAME_COUNT))
        fps = capture.get(cv.CAP_PROP_FPS)
        out_name = 'files/result.avi'
        out = cv.VideoWriter(out_name, four_cc, fps, (frame_width, frame_height), True)
        video_info = {'fps': fps,
                      'video_name': input_video_name,
                      'frame_square': frame_square}

        # Preprocessing
        preprocessing(frames_count, capture, logo, video_info, config)

        # Detection
        stable_contours = detection(video_info, config)

        # Ads insertion
        message = insertion(video_path, frames_count, logo, video_info,
                            config, stable_contours, out, input_video_name)

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
