CC=g++
CFLAGS=-O3 -Wall -shared -fpic
#LDFLAGS=
SOURCES=a_star_cpp.cpp
OBJECTS=$(SOURCES:.cpp=.so)
all:
	$(CC) $(SOURCES) -o $(OBJECTS) $(CFLAGS) $(LDFLAGS)