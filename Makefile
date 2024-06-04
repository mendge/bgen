rm.PHONY: build clean
TARTGET_CMD = bgen

build: prepare
	pyinstaller --onefile main.py --name $(TARTGET_CMD)
	copy dist/$(TARTGET_CMD).exe .

prepare:
	pip install -r requirements.txt

clean:
	rmdir /s /q build dist
	del $(TARTGET_CMD).spec