PROJEKT_NAME = projekt_generisches_faktorisieren_und_dlp
BUILD_DIR = build
BENCHMARK_DLP_RESULT_FILE = projekt/benchmark/results_dlp.txt
BENCHMARK_PARALLEL_RESULT_FILE = projekt/benchmark/results_parallel.txt

all: clean python documentation api_documentation zip

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

api_documentation:
	if [ ! -d "${BUILD_DIR}" ]; then mkdir ${BUILD_DIR}; fi
	sphinx-apidoc -o apidoc/ tocas
	sphinx-apidoc -o apidoc/ ha
	sphinx-apidoc -o apidoc/ projekt
	sphinx-build apidoc build/apidoc

zip:
	cd ${BUILD_DIR}; zip -r ${PROJEKT_NAME}.zip *
	mv build/${PROJEKT_NAME}.zip ${PROJEKT_NAME}.zip

bench_dlp:
	python3 projekt/benchmark/bench_dlp.py > ${BENCHMARK_DLP_RESULT_FILE}

bench_parallel:
	python3 projekt/benchmark/bench_parallel.py > ${BENCHMARK_PARALLEL_RESULT_FILE}

plot_dlp:
	python3 projekt/benchmark/plot.py ${BENCHMARK_DLP_RESULT_FILE}

plot_parallel:
	python3 projekt/benchmark/plot.py ${BENCHMARK_PARALLEL_RESULT_FILE}