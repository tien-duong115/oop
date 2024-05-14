import cv2
import time
import os
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner


class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.update_event = None
        self.fps = fps
        self.frame = None
        self.start()

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            self.frame = frame
            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr'
            )
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture

    def start(self):
        if self.update_event is None:
            self.update_event = Clock.schedule_interval(
                self.update, 1.0 / self.fps)

    def stop(self):
        if self.update_event:
            Clock.unschedule(self.update_event)
            self.update_event = None

    def capture_image(self):
        curr_time = time.strftime('%Y%m%d-%H%M%S')
        export_image_path = os.path.join('screenshot', curr_time + '.png')
        if self.frame is not None:

            cv2.imwrite(export_image_path, self.frame)
            print(f"Image captured and saved as {export_image_path}")
            App.get_running_app().display_img.source = export_image_path


class CamApp(App):
    def build(self):

        main_layout = BoxLayout(orientation="vertical")

        self.my_camera = None
        camera_layout = BoxLayout(size_hint_y=0.8)

        spinner_layout = BoxLayout(size_hint_y=0.1)
        self.spinner = Spinner(
            text='Select Camera',
            values=self.detect_cameras(),
            size_hint=(1, None),
            height=44
        )
        self.spinner.bind(text=self.on_camera_selected)
        spinner_layout.add_widget(self.spinner)
        button_layout = BoxLayout(size_hint_y=0.1)
        start_button = Button(text="Start Camera")
        stop_button = Button(text="Stop Camera")
        capture_button = Button(
            text="Capture",
            size_hint=(None, None),  # Disable size hint to use fixed size
            size=(100, 100),  # Specify the size of the button
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Center the button
        )
        start_button.bind(
            on_press=lambda x: self.my_camera.start() if self.my_camera else None)
        stop_button.bind(on_press=lambda x: self.my_camera.stop()
                         if self.my_camera else None)
        capture_button.bind(
            on_press=lambda x: self.my_camera.capture_image() if self.my_camera else None)
        self.display_img = Image(size_hint_y=0.5)
        main_layout.display_image = self.display_img
        main_layout.add_widget(self.display_img)
        main_layout.add_widget(capture_button)
        main_layout.add_widget(camera_layout)
        button_layout.add_widget(start_button)
        button_layout.add_widget(stop_button)
        main_layout.add_widget(spinner_layout)
        main_layout.add_widget(button_layout)

        return main_layout

    def on_camera_selected(self, spinner, text):
        if self.my_camera:
            self.my_camera.stop()
            self.my_camera.parent.remove_widget(self.my_camera)
        index = int(text)
        self.capture = cv2.VideoCapture(index)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)

        self.root.children[2].add_widget(self.my_camera)

    def on_stop(self):
        if self.my_camera:
            self.my_camera.stop()
        if self.capture:
            self.capture.release()

    def detect_cameras(self):
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                cap.release()
                break
            arr.append(str(index))
            cap.release()
            index += 1
        return arr


if __name__ == "__main__":
    CamApp().run()
