from enum import IntEnum, auto
import typing

from evfl import EventFlow, Actor, ActorIdentifier
from evfl.entry_point import EntryPoint
import PyQt5.QtCore as qc # type: ignore
import PyQt5.QtWidgets as q # type: ignore
import chatgpt_events as cge


class ActorModelColumn(IntEnum):
    Name = 0
    SubName = auto()
    ArgumentName = auto()
    ArgumentEntryPoint = auto()
    NumActions = auto()
    NumQueries = auto()

class ActorModel(qc.QAbstractTableModel):
    def __init__(self, *kwargs) -> None:
        super().__init__(*kwargs)
        self.flow: typing.Optional[EventFlow] = None
        self.l: typing.List[Actor] = []
        self.actors = []

    def set(self, flow):
        self.beginResetModel()
        if hasattr(flow, 'actors'):  # Only access actors if the attribute exists
            self.actors = flow.actors
        else:
            self.actors = []  # Or handle the case where there are no actors differently
        self.endResetModel()

    def rowCount(self, parent=qc.QModelIndex()):
        return len(self.actors)

    def columnCount(self, parent=qc.QModelIndex()):
        return 2  # ID and Name

    def data(self, index, role=qc.Qt.DisplayRole):
        if role == qc.Qt.DisplayRole:
            if index.column() == 0:
                return self.actors[index.row()]['id']
            elif index.column() == 1:
                return self.actors[index.row()]['name']
        return None

    def refresh(self) -> None:
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(None) - 1, self.columnCount(None) - 1))

    def has(self, identifier: ActorIdentifier) -> bool:
        return any(actor.identifier == identifier for actor in self.l)

    def setData(self, index: qc.QModelIndex, value, role) -> bool:
        if role != qc.Qt.EditRole:
            return False
        row = index.row()
        col = index.column()
        actor = self.l[row]

        if col == ActorModelColumn.Name:
            actor.identifier.name = value
            # Optionally regenerate the description when the name changes
            actor.description = cge.generate_text(f"Update the description for actor named {value}")
        elif col == ActorModelColumn.SubName:
            actor.identifier.sub_name = value
        elif col == ActorModelColumn.ArgumentName:
            actor.argument_name = value
        elif col == ActorModelColumn.ArgumentEntryPoint:
            actor.argument_entry_point.v = value

        self.dataChanged.emit(index, index)
        return True

    def appendEmptyActor(self) -> bool:
        if not self.flow or not self.flow.flowchart:
            return False
        self.beginInsertRows(qc.QModelIndex(), len(self.l), len(self.l))
        new_actor = Actor()
        # Generate an initial description for the new actor
        description = cge.generate_text("Generate a description for a new actor")
        new_actor.description = description  # Assuming Actor class has a description attribute
        self.l.append(new_actor)
        self.endInsertRows()
        return True

    def remove(self, actor: Actor) -> bool:
        if not self.flow or not self.flow.flowchart:
            return False
        row = self.l.index(actor)
        if row is None:
            return False
        self.beginRemoveRows(qc.QModelIndex(), row, row)
        self.l.pop(row)
        self.endRemoveRows()
        return True

    def columnCount(self, parent) -> int:
        return len(ActorModelColumn)

    def rowCount(self, parent) -> int:
        return len(self.l)

    def flags(self, index: qc.QModelIndex) -> qc.Qt.ItemFlags:
        if index.column() > ActorModelColumn.ArgumentEntryPoint:
            return super().flags(index)
        return qc.Qt.ItemIsEditable | super().flags(index)

    def setData(self, index: qc.QModelIndex, value, role) -> bool:
        if role != qc.Qt.EditRole:
            return False
        row = index.row()
        col = index.column()
        if col == ActorModelColumn.Name:
            assert isinstance(value, str)
            self.l[row].identifier.name = value
        if col == ActorModelColumn.SubName:
            assert isinstance(value, str)
            self.l[row].identifier.sub_name = value
        if col == ActorModelColumn.ArgumentName:
            assert isinstance(value, str)
            self.l[row].argument_name = value
        if col == ActorModelColumn.ArgumentEntryPoint:
            assert isinstance(value, EntryPoint) or value is None
            self.l[row].argument_entry_point.v = value
        self.dataChanged.emit(index, index)
        return True

    def headerData(self, section, orientation, role) -> qc.QVariant:
        if role != qc.Qt.DisplayRole:
            return qc.QVariant()

        if section == ActorModelColumn.Name:
            return 'Name'
        if section == ActorModelColumn.SubName:
            return 'Sub name'
        if section == ActorModelColumn.ArgumentName:
            return 'Argument name'
        if section == ActorModelColumn.ArgumentEntryPoint:
            return 'Argument entry point'
        if section == ActorModelColumn.NumActions:
            return 'Actions'
        if section == ActorModelColumn.NumQueries:
            return 'Queries'
        return 'Unknown'

    def data(self, index, role) -> qc.QVariant:
        col = index.column()
        row = index.row()

        if role == qc.Qt.UserRole:
            return self.l[row]

        if role == qc.Qt.EditRole:
            if col == ActorModelColumn.Name:
                return self.l[row].identifier.name
            if col == ActorModelColumn.SubName:
                return self.l[row].identifier.sub_name
            if col == ActorModelColumn.ArgumentName:
                return self.l[row].argument_name
            if col == ActorModelColumn.ArgumentEntryPoint:
                return self.l[row].argument_entry_point.v
            return qc.QVariant()

        if role != qc.Qt.DisplayRole and role != qc.Qt.ToolTipRole:
            return qc.QVariant()

        if col == ActorModelColumn.Name:
            return self.l[row].identifier.name
        if col == ActorModelColumn.SubName:
            return self.l[row].identifier.sub_name or '–'
        if col == ActorModelColumn.ArgumentName:
            return self.l[row].argument_name or '–'
        if col == ActorModelColumn.ArgumentEntryPoint:
            if not self.l[row].argument_entry_point.v:
                return '–'
            return str(self.l[row].argument_entry_point.v.name)
        if col == ActorModelColumn.NumActions:
            return str(len(self.l[row].actions))
        if col == ActorModelColumn.NumQueries:
            return str(len(self.l[row].queries))
        return qc.QVariant()
