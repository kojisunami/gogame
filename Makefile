
all : main.c
	gcc -o run main.c -lGLU -lGL -lglut 


debug :
	./run
