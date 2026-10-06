.PHONY: deb install install-local clean test

PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

deb:
	dpkg-buildpackage -b -uc -us

install:
	install -D -m 755 src/chord $(DESTDIR)$(BINDIR)/chord

install-local:
	$(MAKE) install PREFIX=$(HOME)/.local

test:
	python3 tests/test_parser.py
	python3 src/chord --list-chords > /dev/null

clean:
	rm -rf debian/chord debian/.debhelper debian/files
	dh_clean 2>/dev/null || true
	rm -f ../chord_*.deb ../chord_*.buildinfo ../chord_*.changes
