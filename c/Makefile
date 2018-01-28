
ALL = $(sort $(patsubst %.c,%,$(wildcard day*.c)))

.PRECIOUS: %.c %.o
.DEFAULT_GOAL := run

-include Makefile.dep

CC = gcc
CFLAGS = -Wall -Wpedantic -Werror -Winline -g -O3 -Os -march=native

run: $(patsubst %,run-%,$(ALL))

run-%: %
	./$<

valgrind: $(patsubst %,valgrind-%,$(ALL))

valgrind-%: %
	valgrind --leak-check=full ./$<

Makefile.dep:
	gcc -MM *.c > $@

clean:
	rm -f $(ALL)
	rm -f *.o
	rm -f Makefile.dep

day01: day01.o util.o
day02: day02.o util.o
day03: day03.o util.o

day04: LDLIBS = -lcrypto -lssl
day04: day04.o util.o

day05: day05.o util.o
