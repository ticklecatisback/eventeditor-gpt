from enum import IntEnum, auto
import typing
from typing import Union, Any
import threading
from PyQt5 import QtCore as qc, QtWidgets as q
from PyQt5.QtCore import QVariant
from evfl import EventFlow, Event
import chatgpt_events as cge
from eventeditor.util import get_event_type, get_event_description, get_event_next_summary, get_event_param_list

class EventModelColumn(IntEnum):
    Name = 0
    Type = auto()
    Description = auto()
    Next = auto()
    Parameters = auto()

class EventModel(qc.QAbstractTableModel):
    def __init__(self, *kwargs):
        super().__init__(*kwargs)
        self.flow: typing.Optional[EventFlow] = None
        self.l: list = []
        self.events = []

    def set(self, flow):
        self.beginResetModel()
        # Check if the 'events' attribute exists
        if flow and hasattr(flow, 'events'):
            self.events = flow.events
        else:
            self.events = []  # Default to an empty list if no 'events' attribute
        self.endResetModel()

    def rowCount(self, parent=qc.QModelIndex()):
        return len(self.events)

    def columnCount(self, parent=qc.QModelIndex()):
        return 1  # Assuming we're only displaying names

    def data(self, index, role=qc.Qt.DisplayRole):
        if role == qc.Qt.DisplayRole and index.isValid() and 0 <= index.row() < len(self.events):
            return self.events[index.row()]['name']
        return None

    def append(self, event: Event) -> bool:
        self.beginInsertRows(qc.QModelIndex(), len(self.l), len(self.l))
        self.l.append(event)
        self.endInsertRows()
        return True

    def removeRow(self, row: int) -> bool:
        if row < 0 or row >= len(self.l):
            return False
        self.beginRemoveRows(qc.QModelIndex(), row, row)
        self.l.pop(row)
        self.endRemoveRows()
        return True

    def set(self, flow) -> None:
        self.beginResetModel()
        self.flow = flow
        self.l = self.flow.flowchart.events if self.flow and self.flow.flowchart else []
        self.endResetModel()

    def columnCount(self, parent=qc.QModelIndex()) -> int:
        return len(EventModelColumn)

    def rowCount(self, parent=qc.QModelIndex()) -> int:
        return len(self.l)

    def headerData(self, section, orientation, role) -> Union[QVariant, QVariant, str]:
        if role != qc.Qt.DisplayRole:
            return QVariant()

        column = EventModelColumn(section)
        return {
            EventModelColumn.Name: 'Name',
            EventModelColumn.Type: 'Type',
            EventModelColumn.Description: 'Description',
            EventModelColumn.Next: 'Next',
            EventModelColumn.Parameters: 'Parameters'
        }.get(column, 'Unknown')

    def data(self, index, role) -> Union[QVariant, str, Any]:
        if not index.isValid() or not (0 <= index.row() < len(self.l)):
            return QVariant()
        event = self.l[index.row()]
        if role in (qc.Qt.DisplayRole, qc.Qt.ToolTipRole):
            column = EventModelColumn(index.column())
            if column == EventModelColumn.Name:
                return event.name
            elif column == EventModelColumn.Type:
                return get_event_type(event)
            elif column == EventModelColumn.Description:
                return get_event_description(event)
            elif column == EventModelColumn.Next:
                return get_event_next_summary(event)
            elif column == EventModelColumn.Parameters:
                params = get_event_param_list(event)
                return '; '.join([f'{k}={v}' for k, v in params.items()]) if role == qc.Qt.DisplayRole else '<br>'.join(
                    [f'<b>{k}</b>: {v}' for k, v in params.items()])
        return QVariant()

    def generate_event_description(self, event_index):
        if not (0 <= event_index < len(self.l)):
            return
        event = self.l[event_index]
        prompt = f"Generate a description for an event where {event.name}"
        def handle_description(text):
            event.description = text
            idx = self.index(event_index, EventModelColumn.Description)
            self.dataChanged.emit(idx, idx)
        thread = threading.Thread(target=lambda: handle_description(cge.generate_text(prompt)))
        thread.start()
