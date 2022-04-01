#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Avid Log Exchange Table using PySide2 QTableWidget
# Copyright (c) 2021 Bryan Randell
# You can copy and paste cells and Drag and Drop an ALe file to import it
# Borrow code from some sources, mainly some pieces of code Stack Overflow
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QPushButton, QWidget, QTableWidget, QTableWidgetItem, \
    QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QMenuBar, QMainWindow
from PyQt5.QtCore import Qt, pyqtSlot
from pathlib import PureWindowsPath
import platform
import os


def open_and_split_tab_ale_file(ale_file_path: str, encoding:str="ISO-8859-1") -> list:
    ale_file = open(ale_file_path, "r", encoding=encoding)
    string_ale_file = ale_file.read()
    ale_file.close()
    return [line.split("\t") for line in string_ale_file.split("\n")]


def join_and_write_ale_file(list_ale_split_by_tab_and_backspace_string:list, ale_file_path: str,
                            encoding : str ="ISO-8859-1") -> str:
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

"""Create the main window and add the AleTable widget"""
class AleTable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Avid Log Exchange Table")
        self.setGeometry(300, 300, 800, 600)
        self.ale_table_window = AleTableWidget()
        # self.main_layout = QVBoxLayout()

        self.import_ale_file = self.ale_table_window.OnCLickImportAleAndCreateTable
        self.save_ale_file = self.ale_table_window.OnClickSaveAleFile
        self.save_as_ale_file = self.ale_table_window.OnClickSaveAsAleFile
        self.clear_table = self.ale_table_window.clearTable
        self.copy_selected_rows = self.ale_table_window.OnClickCopy
        self.paste_selected_rows = self.ale_table_window.OnClickPaste
        self.cut_selected_rows = self.ale_table_window.OnClickCut
        # self.delete_selected_rows = self.ale_table_window.OnClickDeleteSelectedRows
        self.about = self.ale_table_window.OnClickAbout

        """create a menu bar with file edit and help with import ale, save, save as and clear table"""
        self.menu_bar = QMenuBar(self)

        self.menu_bar.setNativeMenuBar(False)
        # self.menu_bar.setStyleSheet("QMenuBar {background-color: #2d2d2d; color: #f0f0f0; font-size: 12px; font-weight: bold; font-family: Arial; }")
        # self.menu_bar.setFixedHeight(20)
        """File Menu add Import Ale, Save, Save As and Clear Table"""
        self.file_menu = self.menu_bar.addMenu("File")
        self.file_menu.addAction("Import Ale")
        self.file_menu.addAction("Save")
        self.file_menu.addAction("Save As")
        self.file_menu.addAction("Clear Table")
        """Edit Menu add Copy, Paste, Cut, Delete"""
        self.edit_menu = self.menu_bar.addMenu("Edit")
        self.edit_menu.addAction("Copy")
        self.edit_menu.addAction("Paste")
        self.edit_menu.addAction("Cut")
        # self.edit_menu.addAction("Delete")
        """Help Menu add About"""
        self.help_menu = self.menu_bar.addMenu("Help")
        self.help_menu.addAction("About")

        """Connect the import actions to the slots"""
        self.file_menu.actions()[0].triggered.connect(self.import_ale_file)
        self.file_menu.actions()[1].triggered.connect(self.save_ale_file)
        self.file_menu.actions()[2].triggered.connect(self.save_as_ale_file)
        self.file_menu.actions()[3].triggered.connect(self.clear_table)
        """Connect the edit actions to the slots"""
        self.edit_menu.actions()[0].triggered.connect(self.copy_selected_rows)
        self.edit_menu.actions()[1].triggered.connect(self.paste_selected_rows)
        self.edit_menu.actions()[2].triggered.connect(self.cut_selected_rows)
        # self.edit_menu.actions()[3].triggered.connect(self.delete_selected_rows)
        """Connect the help actions to the slots"""
        self.help_menu.actions()[0].triggered.connect(self.about)

        self.setMenuBar(self.menu_bar)
        # self.ale_table_window.setLayout(self.main_layout)
        self.setCentralWidget(self.ale_table_window)
        self.showMaximized()
        # self.show()



class AleTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PySide2 ALE Table'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setAcceptDrops(True)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


        self.main_vertical_layout = QVBoxLayout()
        self.setLayout(self.main_vertical_layout)

        self.table_ale_widget = QTableWidget()

        horizontal_layout_top_bar = QHBoxLayout()

        self.search_item_query = QLineEdit()
        self.search_item_query.setPlaceholderText("Search item in Ale file...")
        self.search_item_query.textChanged.connect(self.search)

        self.clear_table_button = QPushButton()
        self.clear_table_button.setText("CLEAR TABLE")
        self.clear_table_button.clicked.connect(self.clearTable)

        self.import_ale_button = QPushButton()
        self.import_ale_button.setText("IMPORT ALE")
        self.import_ale_button.clicked.connect(self.OnCLickImportAleAndCreateTable)

        horizontal_layout_top_bar.addWidget(self.search_item_query)
        horizontal_layout_top_bar.addWidget(self.clear_table_button)
        horizontal_layout_top_bar.addWidget(self.import_ale_button)


        self.main_vertical_layout.addLayout(horizontal_layout_top_bar)


        self.main_vertical_layout.addWidget(self.table_ale_widget)


        horizontal_layout = QHBoxLayout()

        button_vertical_layout = QVBoxLayout()

        self.insert_row_above_button = QPushButton()
        button_vertical_layout.addWidget(self.insert_row_above_button)
        self.insert_row_above_button.setText("INSERT ROW ABOVE")
        self.insert_row_above_button.clicked.connect(self.insertRowAboveTable)
        self.insert_row_above_button.setToolTip("Insert a Row Above current selected cell")

        self.insert_row_below_button = QPushButton()
        button_vertical_layout.addWidget(self.insert_row_below_button)
        self.insert_row_below_button.setText("INSERT ROW BELOW")
        self.insert_row_below_button.clicked.connect(self.insertRowBelowTable)
        self.insert_row_below_button.setToolTip("Insert a Row Below current selected cell")

        horizontal_layout.addLayout(button_vertical_layout)

        self.save_button = QPushButton()
        horizontal_layout.addWidget(self.save_button)
        self.save_button.setText("ERASE SAVE ALE")
        self.save_button.clicked.connect(self.OnClickSaveAleFile)

        self.save_as_button = QPushButton()
        horizontal_layout.addWidget(self.save_as_button)
        self.save_as_button.setText("SAVE AS...")
        self.save_as_button.clicked.connect(self.OnClickSaveAsAleFile)

        self.main_vertical_layout.addLayout(horizontal_layout)

    """All the keyboard shortcuts"""
    def keyPressEvent(self, event) -> None:
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
            else:
                pass
                # for debugging
                # print("No cells to paste")

        elif event.key() == Qt.Key_X and (event.modifiers() & Qt.ControlModifier):
            self.OnClickCut()

        elif event.key() == Qt.Key_Delete:
            self.table_ale_widget.removeRow(self.table_ale_widget.currentItem())

        elif event.key() == Qt.Key_F and (event.modifiers() & Qt.ControlModifier):
            self.first_current_select_item = self.table_ale_widget.selectedItems()
            self.search_item_query.setText(self.first_current_select_item[0].text())
            self.search_item_query.setFocus()
            self.search_item_query.selectAll()

        elif event.key() == Qt.Key_Escape:
            self.search_item_query.clear()

        elif event.key() == Qt.Key_Return:
            self.search_item_query.clear()

        elif event.key() == Qt.Key_I and (event.modifiers() & Qt.ControlModifier):
            self.OnCLickImportAleAndCreateTable()

        elif event.key() == Qt.Key_S and (event.modifiers() & Qt.ControlModifier):
            self.OnClickSaveAleFile()

    """All the functions for the buttons"""
    def OnClickAbout(self):
        self.about_window = QMessageBox.about(self, "About",
                                              "Avid Log Exchange Table\nCopyright (c) 2020 Bryan Randell\n")


    def OnClickCopy(self):
        self.copied_cells = self.table_ale_widget.selectedItems()
        # copied_cell_text = [i.text() for i in self.copied_cells]
        # print(copied_cell_text)

    def OnClickCut(self):
        self.copied_cells = self.table_ale_widget.selectedItems()
        for cell in self.copied_cells:
            self.table_ale_widget.setItem(cell.row(), cell.column(), QTableWidgetItem(""))

    def OnClickPaste(self):
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
        else:
            pass
            # for debugging
            # print("No cells to paste")


    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event) -> None:
        self.ale_file_path = event.mimeData().urls()[0].toLocalFile()
        self.createAleTable()

    def insertRowAboveTable(self) -> None:
        self.table_ale_widget.insertRow(self.table_ale_widget.currentRow())

    def insertRowBelowTable(self) -> None:
        self.table_ale_widget.insertRow(self.table_ale_widget.currentRow() + 1)

    def clearTable(self) -> None:
        user_input = QMessageBox.question(self, "Save and overwrite ALE",
                                          "Are You sure you want to overwrite the Ale file ?",
                                          QMessageBox.Yes | QMessageBox.Cancel)
        if user_input == QMessageBox.Yes:
            self.table_ale_widget.clear()
        else:
            pass

    def search(self, string_searched) -> None:
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

    def OnClickSaveAsAleFile(self) -> None:
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

    def OnClickSaveAleFile(self) -> None:

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


    def OnCLickImportAleAndCreateTable(self) -> None:
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
        if self.ale_file_path:
            self.createAleTable()


    def createAleTable(self) -> None:
        list_ale_file = open_and_split_tab_ale_file(ale_file_path=self.ale_file_path)
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
    @pyqtSlot()
    def on_click(self):
        # print("\n")
        for currentQTableWidgetItem in self.table_ale_widget.selectedItems():
            pass
            # print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

def main():
    app = QApplication(sys.argv)
    ex = AleTable()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
