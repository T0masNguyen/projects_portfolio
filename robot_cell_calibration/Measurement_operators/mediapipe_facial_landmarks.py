import mediapipe as mp
import itertools
import cv2 as cv
import numpy as np


def findFacialLandmarks(mp_face_mesh, mp_drawing_styles, mp_drawing, img, rgb, draw=True):
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=2,
            refine_landmarks=True,
            min_detection_confidence=0.5) as face_mesh:
        results = face_mesh.process(rgb)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # print('face_landmarks:', face_landmarks)
                mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())
        coords_flm = threeD_coords_FacialLandmarks(mp_face_mesh, results, rgb)
        return coords_flm


def findFacialLandmarks_specialPoints(mp_face_mesh, mp_drawing_styles, mp_drawing, img, rgb, draw=True):
    '''
        Be careful ! Not working ! Mistakes included! function to draw specific facial landmarks

        :param mp_face_mesh:
        :param mp_drawing_styles:
        :param mp_drawing:
        :param img: bgr image
        :param rgb: undistored_rgb image
        :param draw: bool

    '''
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=2,
            refine_landmarks=True,
            min_detection_confidence=0.5) as face_mesh:
        results = face_mesh.process(rgb)

        # -----------------------------------------------------------------------------------------detailed facial landmarks
        LEFT_EYE_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
        RIGHT_EYE_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))
        LIPS_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LIPS)))
        FACE_OVAL_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_FACE_OVAL)))
        LEFT_EYEBROW_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYEBROW)))
        RIGHT_EYEBROW_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYEBROW)))
        # --------------------------------------------------------------------------------combined detailed facial landmarks
        combi_flm = LEFT_EYE_INDEXES
        combi_flm.extend(RIGHT_EYE_INDEXES)
        combi_flm.extend(LIPS_INDEXES)
        combi_flm.extend(FACE_OVAL_INDEXES)
        combi_flm.extend(LEFT_EYEBROW_INDEXES)
        combi_flm.extend(RIGHT_EYEBROW_INDEXES)

        if combi_flm:
            for face_landmarks in results.multi_face_landmarks:
                # for face_landmarks in combi_flm:
                # print('face_landmarks:', face_landmarks)
                # drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
                mp_drawing.draw_landmarks(
                    image=rgb,
                    landmark_list=face_landmarks,
                    connections=None,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=None)

def threeD_coords_FacialLandmarks(mp_face_mesh, results, rgb):
    '''
            function to extract coordinates of specific facial landmarks

            :param mp_face_mesh:
            :param rgb: undistored_rgb image
            :return array_flm: numpy array with lable, image coordinates and object coordinates
    '''

    if results.multi_face_landmarks is not None:
        landmarks = results.multi_face_landmarks[0]

        # -----------------------------------------------------------------------------------------detailed facial landmarks
        LEFT_EYE_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
        RIGHT_EYE_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))
        LIPS_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LIPS)))
        FACE_OVAL_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_FACE_OVAL)))
        LEFT_EYEBROW_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYEBROW)))
        RIGHT_EYEBROW_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYEBROW)))
        # --------------------------------------------------------------------------------combined detailed facial landmarks
        combi_flm = LEFT_EYE_INDEXES
        combi_flm.extend(RIGHT_EYE_INDEXES)
        combi_flm.extend(LIPS_INDEXES)
        combi_flm.extend(FACE_OVAL_INDEXES)
        combi_flm.extend(LEFT_EYEBROW_INDEXES)
        combi_flm.extend(RIGHT_EYEBROW_INDEXES)

        xs = []
        ys = []
        zs = []

        # ----------------------------------------------------------------------array with 2D image coords
        flm_x = np.empty(len(combi_flm))
        flm_y = np.empty(len(combi_flm))

        it = 0
        i = 0

        shape_x = rgb.shape[1]
        shape_y = rgb.shape[0]

        array_flm = []
        for it in combi_flm:
            x = landmarks.landmark[it].x
            y = landmarks.landmark[it].y
            z = landmarks.landmark[it].z

            xs.append(x)
            ys.append(y)
            zs.append(z)

            relative_x = int(x * shape_x)
            relative_y = int(y * shape_y)

            flm_x[i] = relative_x
            flm_y[i] = relative_y

            array_flm.append((np.array([it, flm_x[i], flm_y[i], x, y, z])))
            i = i + 1
        return array_flm
    else:
        return None


if __name__ == '__main__':
    print("unit for facial landmark detection \n \t -> run facial_landmarks_pose_detection.py  \n \t    with option measure_facial_landmarks=True")
