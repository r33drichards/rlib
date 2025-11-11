CC = gcc
CFLAGS = -Wall -Wextra -I../../include
LDFLAGS = -L../../target/release -lrlib

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    LDFLAGS += -Wl,-rpath,@loader_path/../../target/release
else
    LDFLAGS += -Wl,-rpath,$$ORIGIN/../../target/release
endif

example: example.c
	$(CC) $(CFLAGS) -o example example.c $(LDFLAGS)

run: example
	./example

clean:
	rm -f example

.PHONY: run clean
