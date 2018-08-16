PROJEKT_NAME = projekt_generisches_faktorisieren_und_dlp
BUILD_DIR = build
BENCHMARK_RESULT_FILE = projekt/benchmark/results.txt

all: clean python documentation zip

clean:
	rm -rf build
	rm -f ${PROJEKT_NAME}.zip

python:
	if [ ! -d "${BUILD_DIR}" ]; then mkdir ${BUILD_DIR}; fi
	cp -r tocas build/tocas
	rm -rf build/tocas/__pycache__
	rm -rf build/tocas/*.pyc
	rm -rf build/tocas/*.py~
	cp -r ha build/ha
	rm -rf build/ha/__pycache__
	rm -rf build/ha/*.pyc
	rm -rf build/ha/*.py~
	rm -rf build/ha/tests/__pycache__
	rm -rf build/ha/tests/*.pyc
	rm -rf build/ha/tests/*.py~
	cp -r projekt build/projekt
	rm -rf build/projekt/__pycache__
	rm -rf build/projekt/*.pyc
	rm -rf build/projekt/*.py~
	rm -rf build/projekt/tests/__pycache__
	rm -rf build/projekt/tests/*.pyc
	rm -rf build/projekt/tests/*.py~
	rm -rf build/projekt/benchmark/__pycache__
	rm -rf build/projekt/benchmark/*.pyc
	rm -rf build/projekt/benchmark/*.py~

documentation:
	if [ ! -d "${BUILD_DIR}" ]; then mkdir ${BUILD_DIR}; fi
	cd doc; pdflatex dokumentation.tex
	cd doc; pdflatex dokumentation.tex
	cp doc/dokumentation.pdf build/

zip:
	cd ${BUILD_DIR}; zip -r ${PROJEKT_NAME}.zip *
	mv build/${PROJEKT_NAME}.zip ${PROJEKT_NAME}.zip

bench:
	python3 projekt/benchmark/bench_dlp.py > ${BENCHMARK_RESULT_FILE}

plot:
	python3 projekt/benchmark/plot.py ${BENCHMARK_RESULT_FILE}