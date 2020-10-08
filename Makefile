PREFIX=/usr/local/bin
install:
	cp run_ata_pulsar spin_predict.py $(PREFIX)
	chmod 755 /usr/local/bin/run_ata_pulsar
	chmod 755 /usr/local/bin/spin_predict.py
	ln -s -f /usrl/ocal/bin/spin_predict.py /usr/local/bin/spin_predict
