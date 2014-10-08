#!/bin/bash	


for((i = 0;i<10;i++)) do
	python game.py -r 5 -rs 4 -m 10 >> robo4510.csv
	python game.py -r 10 -rs 4 -m 10 >> robo41010.csv
	python game.py -r 5 -rs 4 -m 15 >> robo4515.csv
	python game.py -r 10 -rs 4 -m 15 >> robo41015.csv
	python game.py -r 5 -rs 3 -m 10 >> robo3510.csv
	python game.py -r 10 -rs 3 -m 10 >> robo31010.csv
	python game.py -r 5 -rs 3 -m 15 >> robo3515.csv
	python game.py -r 10 -rs 3 -m 15 >> robo31015.csv
	python game.py -r 5 -rs 2 -m 10 >> robo2510.csv
	python game.py -r 10 -rs 2 -m 10 >> robo21010.csv
	python game.py -r 5 -rs 2 -m 15 >> robo2515.csv
	python game.py -r 10 -rs 2 -m 15 >> robo21015.csv
	python game.py -r 5 -rs 1 -m 10 >> robo1510.csv
	python game.py -r 10 -rs 1 -m 10 >> robo11010.csv
	python game.py -r 5 -rs 1 -m 15 >> robo1515.csv
	python game.py -r 10 -rs 1 -m 15 >> robo11015.csv
done