# MAKEFILE

CC = g++

CPP = -std=c++11

CFLAGS =  `pkg-config --cflags --libs opencv`

PROG = GroundTruth.out


all:
	$(CC) $(CPP) gtruth.cpp $(CFLAGS) -o $(PROG) -g

clean:
	rm -f *.o *~ core $(PROG)


#g++ -std=c++11 -g gtruth.cpp -o GroundTruth.out `pkg-config --libs opencv --cflags opencv`