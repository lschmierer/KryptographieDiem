PROJEKT_NAME = projekt_generisches_faktorisieren_und_dlp

all: clean python zip

clean:
	rm -rf build

python:
	mkdir build
	cp -r tocas build/tocas
	rm -rf build/tocas/__pycache__
	rm -rf build/tocas/tests/__pycache__
	cp -r ha build/ha
	rm -rf build/ha/__pycache__
	rm -rf build/ha/tests/__pycache__
	cp -r projekt build/projekt
	rm -rf build/projekt/__pycache__
	rm -rf build/projekt/tests/__pycache__

zip:
	cd build; zip -r ${PROJEKT_NAME}.zip *
	mv build/${PROJEKT_NAME}.zip ${PROJEKT_NAME}.zip