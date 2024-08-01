#importing turtle module
import turtle

coor_list = open('coordinates.txt', 'r').read().splitlines()
turtle.screensize(canvwidth=1024, canvheight=1024)
turtle.speed(0)
tt = turtle.Turtle(visible=False)
tt.penup()
for coor in coor_list:
	x,y = coor.split(" ")
	tt.goto(int(x), int(y))
	tt.dot(1)
turtle.done()


