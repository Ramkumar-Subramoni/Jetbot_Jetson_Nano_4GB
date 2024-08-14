import cv2
import atexit

class JetbotUsbCamera:
    """
    A class used to acess a custom USB camera for jetbot 4gb.

    ...

    Attributes
    ----------
    device : int
        the device index for the camera (default is 0)
    width : int
        the width of the frame (default is 640)
    height : int
        the height of the frame (default is 480)
    cap : cv2.VideoCapture
        the OpenCV VideoCapture object
    running : bool
        a flag indicating whether the camera is currently running

    Methods
    -------
    _initialize_camera():
        Initializes the camera.
    read():
        Reads a frame from the camera.
    release():
        Releases the camera.
    start():
        Starts the camera.
    stop():
        Stops the camera.
    """

    def __init__(self, device=0, width=640, height=480):
        """
        Constructs all the necessary attributes for the CustomJetbotOpenCvUsbCamera object.

        Parameters
        ----------
            device : int
                the device index for the camera (default is 0)
            width : int
                the width of the frame (default is 640)
            height : int
                the height of the frame (default is 480)
        """

        self.device = device
        self.width = width
        self.height = height
        self.cap = None
        self.running = False
        atexit.register(self.release)  # Ensure the camera is released when the script exits

    def _initialize_camera(self):
        """
        Initializes the camera.

        Raises
        ------
        RuntimeError
            If the camera could not be opened or initialized.
        """

        try:
            print("Initializing camera...")
            self.cap = cv2.VideoCapture(self.device)
            print(f"VideoCapture initialized with device {self.device}")

            if not self.cap.isOpened():
                print("Camera could not be opened.")
                raise RuntimeError('Camera could not be opened.')

            ret, image = self.cap.read()
            print(f"Camera read status: {ret}")

            if not ret:
                print("Could not read image from camera.")
                raise RuntimeError('Could not read image from camera.')

            print("Camera initialized successfully.")
            self.running = True

        except Exception as e:
            print(f"Exception during camera initialization: {e}")
            raise RuntimeError('Could not initialize camera. Please see error trace.')

    def read(self):
        """
        Reads a frame from the camera.

        Returns
        -------
        numpy.ndarray
            The resized frame.

        Raises
        ------
        RuntimeError
            If the camera is not opened or has been stopped.
        """

        if self.cap and self.cap.isOpened() and self.running:
            ret, image = self.cap.read()
            if ret:
                image_resized = cv2.resize(image, (self.width, self.height))
                return image_resized
            else:
                raise RuntimeError('Could not read image from camera')
        else:
            raise RuntimeError('Camera is not opened or has been stopped')

    def release(self):
        """
        Releases the camera.
        """

        if self.cap and self.cap.isOpened():
            self.cap.release()
            print("Camera stopped successfully.")
            self.running = False

    def stop(self):
        """
        Stops the camera.
        """

        self.running = False
        self.release()

    def start(self):
        """
        Starts the camera.
        """

        if not self.running:
            self._initialize_camera()