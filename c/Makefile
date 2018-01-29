
ALL = $(sort $(patsubst %.c,%,$(wildcard day*.c)))

.PRECIOUS: %.c %.o
.DEFAULT_GOAL := run

-include Makefile.dep

CC = gcc
CFLAGS = -Wall -Wpedantic -Werror -Winline -g -march=native

run: build $(patsubst %,run-%,$(ALL))

run-%: %
	./$<

build: $(ALL)

valgrind: build $(patsubst %,valgrind-%,$(ALL))

valgrind-%: %
	valgrind -q --leak-check=full --show-leak-kinds=all --error-exitcode=1 ./$<

Makefile.dep:
	gcc -MM *.c > $@

depcheck:
	pkg-config libcrypto    # ubuntu : libssl-dev
	pkg-config libssl       # ubuntu : libssl-dev
	pkg-config libpcre      # ubuntu : libpcre3-dev or basically build-essential

clean:
	rm -f $(ALL)
	rm -f *.o
	rm -f Makefile.dep

day01: day01.o util.o
day02: day02.o util.o
day03: day03.o util.o

day04: LDLIBS = -lcrypto -lssl
day04: day04.o util.o

day05: LDLIBS = -lpcre
day05: day05.o util.o
