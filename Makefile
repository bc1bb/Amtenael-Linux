AmtenaelLauncher: AmtenaelLauncher.c
	gcc -Os -I /usr/include/python3.6m AmtenaelLauncher.c -o AmtenaelLauncher -lpython3.6m -lpthread -lm -lutil -ldl

AmtenaelLauncher.c: AmtenaelLauncher.py
	cython3 AmtenaelLauncher.py -o AmtenaelLauncher.c --embed

clean:
	rm -f AmtenaelLauncher.c