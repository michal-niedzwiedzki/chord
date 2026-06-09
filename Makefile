.PHONY: deb install clean test

deb:
	dpkg-buildpackage -b -uc -us

install:
	install -m 755 src/chord /usr/local/bin/chord

test:
	python3 tests/test_parser.py
	python3 src/chord --list-chords > /dev/null

clean:
	rm -rf debian/chord debian/.debhelper debian/files
	dh_clean 2>/dev/null || true
	rm -f ../chord_*.deb ../chord_*.buildinfo ../chord_*.changes
