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
    audio_name = 'audio_{}_{}.m4a'.format(filename, idx)
    os.system('ffmpeg -i {} -vn -acodec copy files/{}'.format(video_path, audio_name))
    output = 'output/output_{}_{}.avi'.format(filename, idx)
    os.system('ffmpeg -i files/result.avi -i files/{} -codec copy -shortest {}'.format(audio_name, output))


def get_video_info(capture, logo):
    """
    Get the input video info
    :param capture: video capture object
    :param logo: logo name
    :return: dictionary with video info
    """
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    frame_square = frame_height * frame_width
    frames_count = int(capture.get(cv.CAP_PROP_FRAME_COUNT))
    fps = capture.get(cv.CAP_PROP_FPS)
    logo_h, logo_w, _ = logo.shape
    logo_ratio = logo_h / logo_w

    video_info = {'fps': fps,
                  'width': frame_width,
                  'height': frame_height,
                  'frame_square': frame_square,
                  'logo_ratio': logo_ratio,
                  'frames_count': frames_count}

    return video_info


def preprocessing(capture, video_info, config):
    """
    Model preprocessing
    :param capture: video object
    :param video_info: video info
    :param config: config path
    :return:
    """
    print('Preprocessing is running...')
    data = []
    for i in range(video_info['frames_count']):
        ret, frame = capture.read()
        if ret:

            if i == int(video_info['frames_count'] * 0.25):
                print('25% of the preprocessing is completed.')
            if i == int(video_info['frames_count'] * 0.5):
                print('50% of the preprocessing is completed.')
            if i == int(video_info['frames_count'] * 0.75):
                print('75% of the preprocessing is completed.')

            ad_insertion = AdInsertion(frame, None, i, data, video_info)
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
    instance_insertions = ad_insertion.instance_insertions
    print('Detected {} stable contours.'.format(len(instance_insertions)))
    print('Detection completed.')
    return instance_insertions


def get_instances(video, logo, instances, video_info, config):
    """
    Create instance insertions
    :param video: video path
    :param logo: logo path
    :param instances: array with fields instances
    :param video_info: video info
    :param config: config
    :return: message that describe function output
    """
    if len(instances) != 0:
        capture = cv.VideoCapture(video)
        ids = instances[:, 0]
        for i, frame_index in enumerate(ids):
            capture.set(cv.CAP_PROP_POS_FRAMES, frame_index)
            _, frame = capture.read()
            ad_insertion = AdInsertion(frame, logo, frame_index, None, video_info)
            ad_insertion.build_model(config)
            ad_insertion.insert_ad(instances)
            cv.imwrite('output/instances/{}.png'.format(i), ad_insertion.frame)
        capture.release()
        message = 'Insert templates are ready. Please check the templates for further actions.'
        print(message)
    else:
        message = 'No places to insert ad were found. Please try different video file.'
        print(message)

    return message


def preprocessing_executor(video, logo, config):
    """
    Execute AdInsertion model for logo insertion
    :param video: video name
    :param logo: logo name
    :param config: config path
    :return: message that describes function output
    """
    input_video_name = video.split('.')[0]
    files_path = str(Path.cwd()) + '/files'
    output_path = str(Path.cwd()) + '/output'
    instances_path = output_path + '/instances'
    Path(files_path).mkdir(parents=True, exist_ok=True)
    Path(output_path).mkdir(parents=True, exist_ok=True)
    Path(instances_path).mkdir(parents=True, exist_ok=True)

    capture = cv.VideoCapture(output_path + '/' + video)
    read_logo = cv.imread(output_path + '/' + logo)

    if int(capture.get(cv.CAP_PROP_FPS)) == 0 or read_logo is None:
        message = 'ERROR WHILE ENTERING LOGO OR VIDEO PATH.'
        print(message)
    else:
        # Get input video info
        video_info = get_video_info(capture, read_logo)
        video_info['video_name'] = input_video_name

        # Preprocessing
        preprocessing(capture, video_info, config)

        # Detection
        instances = detection(video_info, config)

        # Get instances
        message = get_instances(output_path + '/' + video,
                                output_path + '/' + logo,
                                instances, video_info, config)
    return message


def insertion_executor(video, logo, config):
    """
    Model insertion method
    :param video: video name
    :param logo: logo path
    :param config: config path
    :return: message that describes insertion result
    """
    video_name = video.split('.')[0]
    output_path = str(Path.cwd()) + '/output'
    files_path = str(Path.cwd()) + '/files'
    instances_path = output_path + '/instances'

    if len(os.listdir(files_path)) != 0:
        list_idx = []
        for filename in os.listdir(instances_path):
            if filename == '.DS_Store':
                continue
            insertion_idx = int(filename.split('.')[0])
            list_idx.append(insertion_idx)

        all_contours = []
        stable_contours = np.load('files/all_instances.npy', allow_pickle=True)
        for i, contour in enumerate(stable_contours):
            if i in list_idx:
                for frame_contour in contour:
                    all_contours.append(frame_contour)
        all_contours = np.array(all_contours)

        if len(all_contours) != 0:
            print('Insertion is running...')
            capture = cv.VideoCapture(output_path + '/' + video)
            read_logo = cv.imread(output_path + '/' + logo)
            video_info = get_video_info(capture, read_logo)
            video_info['video_name'] = video_name
            four_cc = cv.VideoWriter_fourcc(*'FMP4')  # XVID FMP4 X264
            out_name = 'files/result.avi'
            out = cv.VideoWriter(out_name, four_cc, video_info['fps'],
                                 (video_info['width'], video_info['height']), True)

            for i in range(video_info['frames_count']):
                ret, frame = capture.read()
                if ret:

                    if i == int(video_info['frames_count'] * 0.25):
                        print('25% of the insertion is completed.')
                    if i == int(video_info['frames_count'] * 0.5):
                        print('50% of the insertion is completed.')
                    if i == int(video_info['frames_count'] * 0.75):
                        print('75% of the insertion is completed.')
                    if i in all_contours[:, 0]:
                        ad_insertion = AdInsertion(frame, output_path + '/' + logo, i, None, video_info)
                        ad_insertion.build_model(config)
                        ad_insertion.insert_ad(all_contours)
                        out.write(ad_insertion.frame)
                    else:
                        out.write(frame)
                else:
                    break
            add_audio(output_path + '/' + video, video_name)
            capture.release()
            out.release()
            print('Insertion completed.')
            message = 'Video file has been processed.'
            print(message)

            paths = [files_path, instances_path]
            for path in paths:
                for filename in os.listdir(path):
                    file_path = os.path.join(path, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))

        else:
            message = 'There is nothing to insert. Please try different video file.'
            print(message)
    else:
        message = 'Please run Video Preprocessing before Advertisemnt Insertion.'
        print(message)

    return message
