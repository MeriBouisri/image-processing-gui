import cv2



opencv_data = {

    'cvt_color': {
        'title': 'Color Conversion',
        'priority': 0,
        'function': cv2.cvtColor,
        'source_keyword': 'src',
    
        'parameters': {
            'type': {
                'title': 'Type',
                'keyword': 'code',
                'widget': 'combobox',
                'default': 'BGR2GRAY',
                'options': {
                    'BGR2GRAY': cv2.COLOR_BGR2GRAY,
                    'BGR2RGB': cv2.COLOR_BGR2RGB,
                    'BGR2HSV': cv2.COLOR_BGR2HSV,
                    'BGR2LAB': cv2.COLOR_BGR2LAB
                }
            }
        }
    },

    'threshold': {
        'title': 'Threshold',
        'priority': 1,
        'function': cv2.threshold,
        'source_keyword': 'src',
        'return_index': 1,
        'parameters': {
            'type': {
                'title': 'Type',
                'keyword': 'type',
                'widget': 'combobox',
                'default': 'THRESH_BINARY',
                'options': {
                    'THRESH_BINARY': cv2.THRESH_BINARY,
                    'THRESH_BINARY_INV': cv2.THRESH_BINARY_INV,
                    'THRESH_TRUNC': cv2.THRESH_TRUNC,
                    'THRESH_TOZERO': cv2.THRESH_TOZERO,
                    'THRESH_TOZERO_INV': cv2.THRESH_TOZERO_INV,
                    'THRESH_OTSU': cv2.THRESH_OTSU,
                    'THRESH_TRIANGLE': cv2.THRESH_TRIANGLE
                }
            },

            'max_value': {
                'title': 'Upper',
                'keyword': 'maxval',
                'widget': 'slider',
                'min': 0,
                'max': 255,
                'default': 255
            },

            'thresh': {
                'title': 'Lower',
                'keyword': 'thresh',
                'widget': 'slider',
                'min': 0,
                'max': 255,
                'default': 127
            }

        }

    },

    'canny': {
        'title': 'Canny Edge Detection',
        'priority': 2,
        'function': cv2.Canny,
        'source_keyword': 'image',
        'parameters': {
            'threshold1': {
                'title': 'Upper',
                'keyword': 'threshold1',
                'widget': 'slider',
                'min': 0,
                'max': 255,
                'default': 127
            },

            'threshold2': {
                'title': 'Lower',
                'widget': 'slider',
                'keyword': 'threshold2',
                'min': 0,
                'max': 255,
                'default': 127
            }
        }
    },

    'morph': {
        'title': 'Morphological Transformations',
        'priority': 3,
        'function': cv2.morphologyEx,
        'source_keyword': 'src',
        'parameters': {
            'type': {
                'title': 'Type',
                'keyword': 'op',
                'widget': 'combobox',
                'default': cv2.MORPH_OPEN,
                'options': {
                    'MORPH_OPEN': cv2.MORPH_OPEN,
                    'MORPH_CLOSE': cv2.MORPH_CLOSE,
                    'MORPH_GRADIENT': cv2.MORPH_GRADIENT,
                    'MORPH_TOPHAT': cv2.MORPH_TOPHAT,
                    'MORPH_BLACKHAT': cv2.MORPH_BLACKHAT
                }
            },

            'kernel': {
                'title': 'Kernel',
                'keyword': 'kernel',
                'widget': 'unimplemented',
                'default': cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            },

            'iterations': {
                'title': 'Iterations',
                'keyword': 'iterations',
                'widget': 'spinbox',
                'min': 1,
                'max': 10,
                'default': 1
            }
        }
    }
}



