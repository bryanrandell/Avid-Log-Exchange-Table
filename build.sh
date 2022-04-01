source venv/bin/activate
pyinstaller ale_table.py -F \
--name "ale_table_mac" \
--icon="aletable_icon64.ico" \
--hidden-import=PySide2 \
--clean \

