CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -I../../../include
LDFLAGS = -L../../../target/release -lrlib

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    LDFLAGS += -Wl,-rpath,@loader_path/../../../target/release
else
    LDFLAGS += -Wl,-rpath,$$ORIGIN/../../../target/release
endif

test_rlib: test_rlib.cpp
	$(CXX) $(CXXFLAGS) -o test_rlib test_rlib.cpp $(LDFLAGS)

test: test_rlib
	./test_rlib

clean:
	rm -f test_rlib

.PHONY: test clean
