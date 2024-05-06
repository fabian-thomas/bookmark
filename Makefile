ifndef DESTDIR
	DESTDIR = /usr/local
endif

install:
	mkdir -p $(DESTDIR)/bin
	cp -f bin/bookmark bin/dmenu-bookmark bin/rofi-bookmark bin/rofi-bookmark-download.py bin/rofi-bookmark-download bin/rofi-bookmark-download-retry bin/rofi-bookmark-add $(DESTDIR)/bin/
	chmod 755 $(DESTDIR)/bin/bookmark $(DESTDIR)/bin/dmenu-bookmark $(DESTDIR)/bin/rofi-bookmark $(DESTDIR)/bin/rofi-bookmark-download.py $(DESTDIR)/bin/rofi-bookmark-download $(DESTDIR)/bin/rofi-bookmark-download-retry $(DESTDIR)/bin/rofi-bookmark-add

uninstall:
	$(info Don't forget to remove the git hooks if deployed.)
	rm -f $(DESTDIR)/bin/bookmark $(DESTDIR)/bin/dmenu-bookmark $(DESTDIR)/bin/rofi-bookmark $(DESTDIR)/bin/rofi-bookmark-download.py $(DESTDIR)/bin/rofi-bookmark-git-hook $(DESTDIR)/bin/rofi-bookmark-download $(DESTDIR)/bin/rofi-bookmark-download-retry $(DESTDIR)/bin/rofi-bookmark-add
