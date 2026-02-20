from PySide6.QtCore import Qt

def frameMousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
        self._is_dragging = True
        self._drag_start_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        event.accept()

def frameMouseMoveEvent(self, event):
    if self._is_dragging:
        self.move(event.globalPosition().toPoint() - self._drag_start_position)
        event.accept()

def frameMouseReleaseEvent(self, event):
    if event.button() == Qt.LeftButton:
        self._is_dragging = False
        event.accept()
