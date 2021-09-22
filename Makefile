ifndef PREFIX
	PREFIX = /usr/local
endif

install:
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	cp -f bin/bookmark bin/dmenu-bookmark $(DESTDIR)$(PREFIX)/bin/
	chmod 755 $(DESTDIR)$(PREFIX)/bin/bookmark $(DESTDIR)$(PREFIX)/bin/dmenu-bookmark

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/bookmark $(DESTDIR)$(PREFIX)/bin/dmenu-bookmark
