test:
	py.test --tb=short

publish:
	@python setup.py sdist register upload
