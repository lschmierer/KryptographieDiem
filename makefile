PROJEKT_NAME = projekt_generisches_faktorisieren_und_dlp
BUILD_DIR = build

all: clean python documentation zip

clean:
	rm -rf build
	rm -f ${PROJEKT_NAME}.zip

python:
	if [ ! -d "${BUILD_DIR}" ]; then mkdir ${BUILD_DIR}; fi
	cp -r tocas build/tocas
	rm -rf build/tocas/__pycache__
	rm -rf build/tocas/tests/__pycache__
	cp -r ha build/ha
	rm -rf build/ha/__pycache__
	rm -rf build/ha/tests/__pycache__
	cp -r projekt build/projekt
	rm -rf build/projekt/__pycache__
	rm -rf build/projekt/tests/__pycache__

documentation:
	if [ ! -d "${BUILD_DIR}" ]; then mkdir ${BUILD_DIR}; fi
	pdflatex --jobname=doc/dokumentation doc/dokumentation.tex
	pdflatex --jobname=doc/dokumentation doc/dokumentation.tex
	cp doc/dokumentation.pdf build/

zip:
	cd ${BUILD_DIR}; zip -r ${PROJEKT_NAME}.zip *
	mv build/${PROJEKT_NAME}.zip ${PROJEKT_NAME}.zip