import sys
import copy
import math
import random


# Global variables
board_size = 19
#move_count=1
move_count=8

blank=-1
white=0
black=1
white_domain=2
black_domain=3

# main data
board = []
eval_board = []
num_black_prisoner=0
num_white_prisoner=0
num_black_domain=0
num_white_domain=0

# calculation variables
check_list = []
died_list = []


def board_init():
	for loop in range(board_size**2):
		board.append(blank)
	board[3*board_size+3] = black	
	board[4*board_size+3] = black	
	board[5*board_size+3] = black	
	board[2*board_size+3] = black	
	board[2*board_size+4] = black	

	board[3*board_size+2] = white
	board[3*board_size+4] = white
	board[4*board_size+2] = white
	board[4*board_size+4] = white
	board[5*board_size+2] = white
	board[5*board_size+4] = white
	board[6*board_size+3] = white

	board[15*board_size+15] = white

	put_stone(5,2, white)
	put_stone(4,1, white)
	put_stone(3,1, white)


# two starts opening
#	put_stone( 3, 3, white)
#	put_stone( 3,15, white)
#	put_stone(15, 3, black)
#	put_stone(15,15, black)

# joseki
#	put_stone (2,2,black)
#	put_stone (2,3,black)
#	put_stone (2,5,black)
#	put_stone (1,5,black)
#	put_stone (3,2,white)
#	put_stone (3,3,white)
#	put_stone (3,4,white)
#	put_stone (3,5,white)
#	put_stone (3,6,white)
#	put_stone (2,6,white)
#	put_stone (1,6,white)

	#read_sgf("hoge.sgf")

def show_board():
	eval_board_func()

	num_black_domain = 0
	for i in range(0,len(board)):
		if (eval_board [ i] == black_domain):
			num_black_domain += 1

	num_white_domain = 0
	for i in range(0,len(board)):
		if (eval_board [ i] == white_domain):
			num_white_domain += 1

	print ("Go board")
	print ( move_count, "th movement\n")
	
	print("estimated black score: ", num_black_domain-num_black_prisoner)
	print("estimated white score: ", num_white_domain-num_white_prisoner)
	print("")

	print ( "    0|0|0|0|0|0|0|0|0|1|1|1|1|1|1|1|1|1|1")
	print ( "    1|2|3|4|5|6|7|8|9|0|1|2|3|4|5|6|7|8|9")

	for y in range(0,board_size):
		sys.stdout.write(str(format(y+1,"02")))
		sys.stdout.write("|")
		for x in range(0,board_size):
			sys.stdout.write(" ")
			if (eval_board[y*board_size+x] == blank):
				if  ((y%6==3)  and (x%6==3)): # draw the star point 
					sys.stdout.write("\033[1;37;40mx\033[1;37;40m")
				else:
					sys.stdout.write("\033[1;37;40m.\033[1;37;40m")
			elif (eval_board[y*board_size+x] == black):
				sys.stdout.write("\033[1;31;40m\u25CF\033[1;37;40m")
			elif (eval_board[y*board_size+x] == white):
				sys.stdout.write("\033[1;32;40m\u25CF\033[1;37;40m")
			elif (eval_board[y*board_size+x] == black_domain):
				sys.stdout.write("\033[1;31;40m.\033[1;37;40m")
			elif (eval_board[y*board_size+x] == white_domain):
				sys.stdout.write("\033[1;32;40m.\033[1;37;40m")
		sys.stdout.write("\n")


def read_sgf(filename):
	global board
	fd = open(filename, "r+")
	string = fd.read()
	
	sgf_dat = string.split(";")

	sgf_dat.pop(0)
	sgf_dat.pop(0)

	board = []
	for i in range(0, board_size**2):
		board.append(blank)

	for i in range(0,len(sgf_dat)):
		if ( sgf_dat[i][0] == 'B'):
			p = black
		if ( sgf_dat[i][0] == 'W'):
			p = white
		x = ord(sgf_dat[i][2]) - 0x60
		y = ord(sgf_dat[i][3]) - 0x60
		#print ("(x, y):", x, y)
		board[(y-1)*board_size +(x-1)] = p


def put_stone(x,y, color):
	board[y*board_size+x] = color




for i in range(board_size*board_size):
	check_list.append(True)


# This function measures the domain of black and white.
# This function identifies which player have an advantage for each blank area
def eval_board_func():
	global board
	global eval_board
	eval_board = copy.deepcopy(board)
	for y in range(0, board_size):
		for x in range(0, board_size):
			eval_board[y*board_size+x] = _eval_board_func(x,y)
			 


# If the score is positive, it is possibly the domain of white,
# and if negative, it is the domain of black
# The domain evaluation method is \sum \frac{1}{/sqrt{i^2+j^2}}
def _eval_board_func (x_offset, y_offset):
	domain_score = 0
	search_length = 5
	offset= y_offset*board_size + x_offset
	if ( board[offset] != blank):
		return board[offset]
	for i in range(-search_length, search_length):
		for j in range(-search_length+abs(i), search_length-abs(i)):
			target_pt = offset + j*board_size + i
			if ((x_offset +i >= 0) 
				and (x_offset + i < board_size)
				and (y_offset + j >= 0)
				and (y_offset + j < board_size)):
				if (board[target_pt]== black):
					domain_score -= 1/ math.sqrt((i*i) + (j*j))
				elif (board[target_pt]== white):
					domain_score += 1/ math.sqrt((i*i) + (j*j))

	threshold = 0.3
	if (domain_score > threshold): # white's advantage
		return white_domain
	elif ((domain_score < threshold ) and (domain_score > -threshold)): #neutral
		return blank
	else:
		return black_domain
				

	
def check_stone_life (x_offset,y_offset, color):

	global check_list
	global died_list
	global num_black_prisoner
	global num_white_prisoner

	check_list = []
	died_list = []

	#initialization
	if ((x_offset >= 19) or ( x_offset < 0)):
		return 
	if ((y_offset >= 19) or ( y_offset < 0)):
		return 

	for i in range(board_size*board_size):
		check_list.append(True)

	offset = y_offset*board_size+x_offset;

	#return _check_stone_life(offset, color)
	if _check_stone_life(offset, color):
		if(color%2== black):
			num_black_prisoner += len(died_list)
		else:
			num_white_prisoner += len(died_list)
		for i in range(len(died_list)):
			board[died_list[i]] = blank


# We will find a cluster that contains (x,y)
# If returns True, the stone is died
def _check_stone_life ( offset, color):
	died_list.append(offset)

	# if the output is True, the direction is died,
	# if four directions are died, the stone is died.
	def check_direction( d ):
		if (((offset%board_size == 0) and d == -1) or # this is on the edge
			((offset%board_size == board_size-1) and d==1) or
			((int(offset/board_size) <= 0) and d==-board_size) or
			((int(offset/board_size) >= board_size-1) and d==board_size)):
			return True
		else:
			if (board[offset+d] == blank):
				return False
			elif (board[offset+d] == (color+1)%2):
				return True
			else:
				check_list[offset] = False
				if (check_list[offset+d] == True):
					return _check_stone_life( offset+d, color)
				else:
					return True

	return ( 
		check_direction(-1) and
		check_direction(1) and
		check_direction(-board_size) and
		check_direction(board_size) )







##########################################################################
#
# Behavior
#
#
#
##########################################################################

board_init()
eval_board_func()
show_board()

while True:


	if(move_count%2 == black):
		print("this is black's turn")
	if(move_count%2 == white):
		print("this is white's turn")
	print("input the next movement")

	while True:
		x = input("x?")
		y = input("y?")
		if not x.isdigit():
			print ("input integer again")
			continue
		if not y.isdigit():
			print ("input integer again")
			continue
		x = int(x)
		y = int(y)
		print (y)
		if (( x == 0 ) and (y==0)):
			move_count+=1
			break
		if ((x<1) or (x>board_size)):
			print("input number in range (1..19)")
			continue
		if ((y<1) or (y>board_size)):
			print("input number in range (1..19)")
			continue
		if( board[(y-1)*board_size+(x-1)] != blank):
			print("there is a stone already")
			continue
	
		put_stone( x-1, y-1, move_count%2)

		check_stone_life(x-1-1,y-1, (move_count+1)%2)
		check_stone_life(x-1+1,y-1, (move_count+1)%2)
		check_stone_life(x-1,y-1-1, (move_count+1)%2)
		check_stone_life(x-1,y-1+1, (move_count+1)%2)


		show_board()
		move_count +=1
		break


	#if not check_stone_life(x-1,y-1,move_count%2):
		#print("this is a suicide")
		#continue

	#for j in range(board_size):
	#	for i in range(board_size):
	#		if not check_stone_life(j, i, move_count%2+1):
	#			print("surrounded, the stone is dead", i+1, ",", j+1)



	# this is black's turn
	while True:
		bx = random.randrange(0,19)
		by = random.randrange(0,19)
		if (board[ by*board_size + bx] != blank ) :
			continue
		else:
			put_stone( bx, by, move_count%2)
		
			check_stone_life(x-1-1,y-1, (move_count+1)%2)
			check_stone_life(x-1+1,y-1, (move_count+1)%2)
			check_stone_life(x-1,y-1-1, (move_count+1)%2)
			check_stone_life(x-1,y-1+1, (move_count+1)%2)
			show_board()
			move_count += 1

			break










