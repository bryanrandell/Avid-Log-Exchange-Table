#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Avid Log Exchange Table using PySide2 QTableWidget
# Copyright (c) 2021 Bryan Randell
# Borrow code from some sources, mainly some pieces of code Stack Overflow


import sys
from PySide2.QtWidgets import QApplication, QFileDialog, QPushButton, QWidget, QTableWidget, \
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox
from PySide2.QtCore import Slot, Qt
from pathlib import PureWindowsPath
import platform
import os


def open_and_split_tab_ale_file(ale_file_path = "ALE/A043CWGY.ale", encoding="ISO-8859-1"):
    ale_file = open(ale_file_path, "r", encoding=encoding)
    string_ale_file = ale_file.read()
    ale_file.close()
    return [line.split("\t") for line in string_ale_file.split("\n")]


def join_and_write_ale_file(list_ale_split_by_tab_and_backspace_string, ale_file_path="ALE/test.ale", encoding="ISO-8859-1"):
    reformed_string_with_backspace = ""
    line_counter = 0
    for line in list_ale_split_by_tab_and_backspace_string:
        reformed_string_with_backspace += "\t".join(line)
        line_counter += 1
        if line_counter < len(list_ale_split_by_tab_and_backspace_string):
            reformed_string_with_backspace += "\n"

    ale_file = open(ale_file_path, "w", encoding=encoding)
    ale_file.write(reformed_string_with_backspace)
    ale_file.close()
    return reformed_string_with_backspace



class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PySide2 ALE Table'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


        self.main_vertical_layout = QVBoxLayout()
        self.setLayout(self.main_vertical_layout)

        self.table_ale_widget = QTableWidget()
        self.main_vertical_layout.addWidget(self.table_ale_widget)


        honrizontal_layout = QHBoxLayout()

        self.insert_row_above_button = QPushButton()
        honrizontal_layout.addWidget(self.insert_row_above_button)
        self.insert_row_above_button.setText("INSERT ROW ABOVE")
        self.insert_row_above_button.clicked.connect(self.insertRowAboveTable)
        self.insert_row_above_button.setToolTip("Insert a Row Above current selected cell")

        self.insert_row_below_button = QPushButton()
        honrizontal_layout.addWidget(self.insert_row_below_button)
        self.insert_row_below_button.setText("INSERT ROW BELOW")
        self.insert_row_below_button.clicked.connect(self.insertRowBelowTable)
        self.insert_row_below_button.setToolTip("Insert a Row Below current selected cell")

        self.clear_table_button = QPushButton()
        honrizontal_layout.addWidget(self.clear_table_button)
        self.clear_table_button.setText("CLEAR TABLE")
        self.clear_table_button.clicked.connect(self.clearTable)

        self.search_item_query = QLineEdit()
        honrizontal_layout.addWidget(self.search_item_query)
        self.search_item_query.setPlaceholderText("Search item in Ale file...")
        self.search_item_query.textChanged.connect(self.search)

        self.save_button = QPushButton()
        honrizontal_layout.addWidget(self.save_button)
        self.save_button.setText("ERASE SAVE ALE")
        self.save_button.clicked.connect(self.OnclickSaveButton)

        self.save_as_button = QPushButton()
        honrizontal_layout.addWidget(self.save_as_button)
        self.save_as_button.setText("SAVE AS...")
        self.save_as_button.clicked.connect(self.OnclickSaveAsButton)

        self.import_ale_button = QPushButton()
        honrizontal_layout.addWidget(self.import_ale_button)
        self.import_ale_button.setText("IMPORT ALE")
        self.import_ale_button.clicked.connect(self.OnCLickImportAleAndCreateTable)

        self.main_vertical_layout.addLayout(honrizontal_layout)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            self.copied_cells = self.table_ale_widget.selectedItems()
            # copied_cell_text = [i.text() for i in self.copied_cells]
            # print(copied_cell_text)
        elif event.key() == Qt.Key_V and (event.modifiers() & Qt.ControlModifier):
            if self.copied_cells:
                if len(self.copied_cells) == 1:
                    self.paste_cells = self.table_ale_widget.selectedItems()
                    for cell_paste in self.paste_cells:
                        self.table_ale_widget.setItem(cell_paste.row(), cell_paste.column(),
                                                      QTableWidgetItem(self.copied_cells[0].text()))
                else:
                    row = self.table_ale_widget.currentRow() - self.copied_cells[0].row()
                    column = self.table_ale_widget.currentColumn() - self.copied_cells[0].column()
                    for cell in self.copied_cells:
                        self.table_ale_widget.setItem(cell.row() + row, cell.column() + column, QTableWidgetItem(cell.text()))

    def insertRowAboveTable(self):
        self.table_ale_widget.insertRow(self.table_ale_widget.currentRow())

    def insertRowBelowTable(self):
        self.table_ale_widget.insertRow(self.table_ale_widget.currentRow() + 1)

    def clearTable(self):
        user_input = QMessageBox.question(self, "Save and overwrite ALE",
                                          "Are You sure you want to overwrite the Ale file ?",
                                          QMessageBox.Yes | QMessageBox.Cancel)
        if user_input == QMessageBox.Yes:
            self.table_ale_widget.clear()
        else:
            pass

    def search(self, string_searched):
        # clear current selection.
        self.table_ale_widget.setCurrentItem(None)

        if not string_searched:
            # Empty string, don't search.
            return

        matching_items = self.table_ale_widget.findItems(string_searched, Qt.MatchContains)
        if matching_items:
            # we have found something
            for item in matching_items:
                item.setSelected(True)
            # item = matching_items[0]  # take the first
            # self.tableWidget.setCurrentItem(item)

    def OnclickSaveAsButton(self):

        row = 0
        column = 0
        new_ale_list = []
        for i in range(self.table_ale_widget.rowCount()):
            new_line = []
            for x in range(self.table_ale_widget.columnCount()):
                try:
                    text = str(self.table_ale_widget.item(row, column).text())
                    new_line.append(text)
                    column += 1
                except AttributeError:
                    column += 1
            new_ale_list.append(new_line)
            column = 0
            row += 1

        file_filter = 'All File (*.*);; ALE File (*.ale )'
        if platform.system() == "Windows":
            ale_save_file_path, _ = PureWindowsPath(QFileDialog.getSaveFileName(parent=self,
                                                                                caption="Save your ALE file",
                                                                                directory=os.getcwd(),
                                                                                filter=file_filter,
                                                                                initialFilter="ALE File (*.ale )"))
        else:
            ale_save_file_path, _ = QFileDialog.getSaveFileName(parent=self,
                                                                caption="Save your ALE file",
                                                                directory=os.getcwd(),
                                                                filter=file_filter,
                                                                initialFilter="ALE File (*.ale )")

        reformed_string_with_backspace = join_and_write_ale_file(new_ale_list, ale_file_path=ale_save_file_path)
        # print(reformed_string_with_backspace)

    def OnclickSaveButton(self):

        row = 0
        column = 0
        count_item_not_null = 0
        for i in range(self.table_ale_widget.rowCount()):
            for j in range(self.table_ale_widget.columnCount()):
                if self.table_ale_widget.item(row, column):
                    count_item_not_null += 1
                column += 1
            column = 0
            row += 1

        if count_item_not_null > 0:
            user_input = QMessageBox.question(self, "Save and overwrite ALE",
                                              "Are You sure you want to overwrite the Ale file ?",
                                              QMessageBox.Yes | QMessageBox.Cancel)
            if user_input == QMessageBox.Yes:
                row = 0
                column = 0
                new_ale_list = []
                for i in range(self.table_ale_widget.rowCount()):
                    new_line = []
                    for x in range(self.table_ale_widget.columnCount()):
                        try:
                            text = str(self.table_ale_widget.item(row, column).text())
                            new_line.append(text)
                            # self.sheetBook.write(row, col, text)
                            column += 1
                        except AttributeError:
                            column += 1
                    new_ale_list.append(new_line)
                    column = 0
                    row += 1
                reformed_string_with_backspace = join_and_write_ale_file(new_ale_list, ale_file_path=self.ale_file_path)
            else:
                pass
        else:
            QMessageBox.about(self, "ALE file empty", "The ALE file is empty")


    def OnCLickImportAleAndCreateTable(self):
        # Create table
        file_filter = 'All File (*.*);; ALE File (*.ale )'

        if platform.system() == "Windows":
            self.ale_file_path, _ = PureWindowsPath(QFileDialog.getOpenFileName(parent=self,
                                                                                caption="Select an ALE file",
                                                                                directory=os.getcwd(),
                                                                                filter=file_filter,
                                                                                initialFilter="ALE File (*.ale )"))
        else:
            self.ale_file_path, _ = QFileDialog.getOpenFileName(parent=self,
                                                                caption="Select an ALE file",
                                                                directory=os.getcwd(),
                                                                filter=file_filter,
                                                                initialFilter="ALE File (*.ale )")

        # print(self.ale_file_path)
        ale_file_path = self.ale_file_path
        list_ale_file = open_and_split_tab_ale_file(ale_file_path=ale_file_path)
        # print(list_ale_file)
        self.table_ale_widget.clear()
        self.table_ale_widget.setRowCount(len(list_ale_file))
        self.table_ale_widget.setColumnCount(len(max(list_ale_file, key=len)))
        for index_x, line in enumerate(list_ale_file):
            for index_y, element in enumerate(line):
                self.table_ale_widget.setItem(index_x, index_y, QTableWidgetItem(element))

        self.table_ale_widget.move(0, 0)
        self.table_ale_widget.adjustSize()
        # print(self.tableWidget.geometry())
        self.adjustSize()

        self.table_ale_widget.doubleClicked.connect(self.on_click)


    # Using this method only with terminal output
    @Slot()
    def on_click(self):
        # print("\n")
        for currentQTableWidgetItem in self.table_ale_widget.selectedItems():
            pass
            # print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
