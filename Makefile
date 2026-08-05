# airlock-www — the Airlock website.
#
# There is no build step: the site is HTML and CSS, served as written. These
# targets are for working on it, not for producing it.

.PHONY: serve check

serve:                          ## serve the site at http://localhost:8000
	python3 -m http.server 8000 --bind 127.0.0.1

check:                          ## verify the site's structural invariants
	@python3 scripts/check.py
