maint:
	pre-commit autoupdate && pre-commit run --all-files
	pip-compile -U requirements/ci.in
	pip-compile -U requirements/dev.in

upload:
	make clean
	python setup.py sdist bdist_wheel && twine upload dist/*

clean:
	python setup.py clean --all
	pyclean .
	rm -rf *.pyc build dist tests/reports docs/build .pytest_cache .tox .coverage html/
