#TASK 1
sin(2*pi)
cos(3/4)
tan(pi)
log10(100)
log(15)
log(7, 1/7)
exp(3)
64^(1/3)

#TASK 2
seq(1, 10, 1)
sum(seq(1, 10, 1))
sum(1:10)

#TASK 3
#a)
x=seq(2, 20, 2)
x^2
x*x #multiplication of elements in vector, not vectors
#b)
x=rev(x)
x
#c)
sum(x)
#d)
length(x)
#e)
sqrt(sum(x^(2)))

#TASK 4
y=seq(5, 10, length = 13)
y
length(y)

#TASK 5
z1=rep(c(1, 2), 5)
z1
z2=rep(c(1, 2), each=5)
z2

#TASK 6
a=c(1, 3, 6, 2, 7, 4)
#a)
min(a)
#b)
which.min(a)
#c)
a[a<=4]
#d)
sum(a)
#e)
sum(a*a)
#f)
sqrt(sum(a^2))
#g)
a[3]
#h)
a+4 #in R vector + number means increasing each element in vector by this number
#i)
b=a[-4]
b
#j)
c=a+b #a is longer than b so in sixth element R again takes first element from b (circulation)
#k)
d=a[a>4]
d

#TASK 7
M=rbind(c(2, 3, 0), c(1, -1, 2), c(1, 1, -1))
#a)
t(M)
#b)
det(M)
#c)
sum(diag(M))
#d)
M*M
M%*%M
#e)
M*diag(M)
M%*%diag(M)
#f)
N=solve(M)
N
N%*%M
#g)
a=M[,3] #third column
a
#h)
b=M[2,] #second row
b
#i)
t(a)%*%b #scalar
a%*%t(b) #matrix

#TASK 8:
x=seq(1, 10) #x=1:10
y=seq(1, 10)^(1/2)
#a)
plot(seq(1, 10), seq(1, 10)^2, main="f(x)=x^2")
plot(x, y, main="f(x)=x^(1/2)", xlab="x values", ylab="y values")
points(x, y,pch=21, col="blue", bg="white", cex=.5)
#main -> title
#xlab/ylab -> name of x or y-axis
#type -> type of graph ("l" = line, "p" = points, "b" = both line and points, "s" = stairs)
#pch -> shape of the symbol e. g. pch=8 -> "*"
#col -> color of the graph (or of the )
#bg -> background
#cex -> size of point
#lwd -> size of 

#b)
data.frame(x, y)
plot(data.frame(x, y))
#c)
plot(cbind(x, y))

#TASK 9:
curve(x^2 + 3*x - 5, -3, 4, main="My title", xlab="x-axis", y="y-axis", col="green")
curve(x*1+3, col="red", -3, 2, add=TRUE)
