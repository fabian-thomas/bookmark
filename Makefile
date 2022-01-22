ifndef PREFIX
	PREFIX = /usr/local
endif

install:
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	cp -f bin/bookmark bin/dmenu-bookmark bin/rofi-bookmark bin/rofi-bookmark-download.py bin/rofi-bookmark-download bin/rofi-bookmark-download-retry bin/rofi-bookmark-add $(DESTDIR)$(PREFIX)/bin/
	chmod 755 $(DESTDIR)$(PREFIX)/bin/bookmark $(DESTDIR)$(PREFIX)/bin/dmenu-bookmark $(DESTDIR)$(PREFIX)/bin/rofi-bookmark $(DESTDIR)$(PREFIX)/bin/rofi-bookmark-download.py $(DESTDIR)$(PREFIX)/bin/rofi-bookmark-download $(DESTDIR)$(PREFIX)/bin/rofi-bookmark-download-retry $(DESTDIR)$(PREFIX)/bin/rofi-bookmark-add

uninstall:
	$(info Don't forget to remove the git hooks if deployed.)
	rm -f $(DESTDIR)$(PREFIX)/bin/bookmark $(DESTDIR)$(PREFIX)/bin/dmenu-bookmark $(DESTDIR)$(PREFIX)/bin/rofi-bookmark $(DESTDIR)$(PREFIX)/bin/rofi-bookmark-download.py $(DESTDIR)$(PREFIX)/bin/rofi-bookmark-git-hook $(DESTDIR)$(PREFIX)/bin/rofi-bookmark-download $(DESTDIR)$(PREFIX)/bin/rofi-bookmark-download-retry $(DESTDIR)$(PREFIX)/bin/rofi-bookmark-add
