import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit
import evfl
import chatgpt_events as cge

class FlowchartEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_flowchart("ArrowMeister_Momo.bfevfl")

    def init_ui(self):
        self.setWindowTitle("Flowchart Editor")
        layout = QVBoxLayout(self)

        self.actor_name_input = QLineEdit(self, placeholderText="Enter actor name")
        layout.addWidget(self.actor_name_input)

        self.add_actor_button = QPushButton("Add Actor", clicked=self.add_actor)
        layout.addWidget(self.add_actor_button)

        self.add_event_button = QPushButton("Add Event with Description", clicked=self.add_event_with_description)
        layout.addWidget(self.add_event_button)

        self.status_display = QTextEdit(readOnly=True)
        layout.addWidget(self.status_display)

    def load_flowchart(self, filepath):
        self.flow = evfl.EventFlow()
        try:
            with open(filepath, 'rb') as file:
                self.flow.read(file.read())
            self.status_display.append("Flowchart loaded successfully.")
        except Exception as e:
            self.status_display.append(f"Failed to load flowchart: {str(e)}")
            self.flow = None

    def add_actor(self):
        actor_name = self.actor_name_input.text().strip()
        if not actor_name:
            self.status_display.append("Please enter a valid actor name.")
            return

        if not self.flow:
            self.status_display.append("Flowchart is not loaded.")
            return

        try:
            # Initialize Actor without passing the identifier directly to the constructor
            new_actor = evfl.Actor()
            # Assuming Actor has an identifier attribute that we can set after instantiation
            new_actor.identifier = evfl.ActorIdentifier(name=actor_name)
            self.flow.flowchart.actors.append(new_actor)
            self.status_display.append(f"Added actor: {actor_name}")
        except Exception as e:
            self.status_display.append(f"Error adding actor: {str(e)}")
            print(f"Error adding actor: {str(e)}")

    def add_event_with_description(self):
        actor_name = self.actor_name_input.text().strip()
        actor = self.find_actor_by_id(actor_name)
        if not actor:
            self.status_display.append(f"No actor found with the name {actor_name}")
            return

        description = cge.generate_text("Generate a description for an event involving " + actor_name)
        new_event = evfl.Event()
        # Assuming setting a description directly is possible; otherwise, adapt this part based on your evfl library's capabilities
        if hasattr(new_event, 'set_description'):
            new_event.set_description(description)
        elif hasattr(new_event, 'metadata'):
            new_event.metadata['description'] = description
        self.flow.flowchart.events.append(new_event)
        self.status_display.append(f"Event added with description: {description}")

    def find_actor_by_id(self, actor_name):
        if self.flow:
            for actor in self.flow.flowchart.actors:
                if actor.identifier.name == actor_name:
                    return actor
        return None

def main():
    app = QApplication(sys.argv)
    editor = FlowchartEditor()
    editor.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
