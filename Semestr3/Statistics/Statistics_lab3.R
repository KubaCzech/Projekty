#arm package
library("arm")

#TASK 1:
rbinom(1, 30, 0.3)
rbinom(1, 30, 0.5) #increasing p increases number of successes

set.seed(156035)
rbinom(1, 30, 0.3)

#TASK 2:
par(mfrow = c(1, 2))
n = 30
p = 0.3
x = 0:n

set.seed(156035)
a = rbinom(10000, 30, 0.3) #for bigger numbers, e. g. 10000 instead of 20 random binomial distribution is closer to ideal binomial distribution
discrete.histogram(a, xlim = c(0, 30))
plot(dbinom(x, n, p), type = "h") #how binomial distribution looks like

#TASK 3:
n = 5
p = 0.3

print ("S - random variable")
print ("S - number of contaminated wells")
print ("S~ bin(5, 0.3)")

x = 0:n
prob = dbinom(x, n, p)
prob

out = rbind(x, prob) #merging number of contaminated wells with probability
print (out)
#a) 
print(paste("Probability of 3 wells being contaminated is", prob[x==3]))
#b)
print (paste("Probability of at least 3 wells being contaminated is", sum(prob[x>=3])))
#c)
print (paste("Probability of less than 3 wells being contaminated is", sum(prob[x<3])))

#TASK 4:
n = 8
x = 0:n
p = 0.9

B = dbinom(x, n, p)
out = rbind(x, B)
out
#a)
print (B[x == 8])
#b)
print (B[x == 7])
#c)
print (sum(B[x > 5]))
#d)
expectation = sum(B*x)
print (expectation)

#e)
exp2 = sum(B*x*x)
print(paste("Standard dev is:", (exp2 - expectation^2)^(1/2)))

#second way
print(paste("Expectation in this ditribution is: ", n*p))
print(paste("Standard deviation in this ditribution is: ", sqrt(n*p*(1-p))))

#TASK 5:
par(mfrow = c(1, 1))
rm (x) #remove x from our data

lambda = 0.01
curve(dexp(x, lambda), 0, 1000)

#a)
print(paste("Probability that satelite will survive for at least 200 days is:", round((1 - pexp(200,lambda)), 3)))
#b)
print(paste("Probability that satelite will fail in 100 days is:", round(pexp(100,lambda), 3)))
#c)
print(paste("Probability that satelite will fail before 500 days is:", round(pexp(500,lambda), 3))) #we have continous not discrete values so we don't know if it didn't fail in 499.75 days - that's why we need 500

#TASK 6:
mn = 2.4
lambda = 1/mn #f(x) = lambda*e^(lambda*x) == 1/mn * e^(x/mn) where lambda = 1/mn

curve(dexp(x, lambda), 0,4/lambda)
print("X is ..., it represents ...")

#a)
print (1-pexp(3, lambda)) #pexp(3, lambda) -> probability that earthquake will be less than 3; 1-pexp(3, lambda) -> will exceed 3
#b)
print (round(pexp(3, lambda) - pexp(2, lambda), 4)) #P(2<X<3) = P(3) - P(2)
#Verifying:
f = function(x){lambda * exp(-1*lambda * x)}
f
integrate(f, 0, 3)

#TASK 7:
#A ~N(mu, sigma), A is random variable
mu = 0.13
sig = 0.005
print("A is a distribution of wire resistance")
curve(dnorm(x, mu, sig), mu-3*sig, mu+3*sig) #rule of 3 sigma - this interval covers 98%
#pnorm is area under dnorm
# P(0.12 <= A <= 0.14) = F(0.14) - F(0.12)
print(paste("Probability that A will meet specification, is in <0.12, 0.14>, is equal to ", round((pnorm(0.14, mu, sig) - pnorm(0.12, mu, sig)), 4)))
#larger sigma is larger probability of failure

#TASK 8:
#A - drying time
#A ~N(120, 15) -> time in minutes
mu = 120
sig = 15
print("A is drying time")
print(paste("Mean: ", mu, ", Standard deviation: ", sig, sep = ""))
curve(dnorm(x, mu, sig), mu - 3*sig, mu+3*sig)
#P(110 < A < 135) = F(135) - F(110)
print(paste("Probability that A is in <110, 135> is equal to ", round((pnorm(135, mu, sig) - pnorm(110, mu, sig)), 4)))

#TASK 9:
#S = maximum speed
#S~N(46.8, 1.75)
mu = 46.8
sig = 1.75

#a)
#P(S <= 50)
print (paste("Probability that speed is at most 50:", pnorm(50, mu, sig)))

#b)
#P(S < 48) = 1-P(S>= 48)
print (paste("Probability that speed is at least 48:", 1 - pnorm(48, mu, sig)))

curve(dnorm(x, mu, sig), mu - 3*sig, mu + 3*sig)

#TASK 10:
# A is some random variable
#A~bin(20, 0.2)
#we generate 500 numbers
size = 500
n = 20
p = 0.2
numbers = rbinom(size,n, p)
par(mfrow = c(1, 3))
discrete.histogram(numbers, xlim = c(0, n))

y = 0:n
plot(dbinom(y, n, p), type = "h")
mu = n*p
sig = (n*p*(1-p))^(1/2)
curve(dnorm(x, mu, sig), 0, n)

#b)
par(mfrow = c(1, 1))
hist(numbers, xlim = c(0, n), freq = FALSE, col = "blue")
curve(dnorm(x, mu, sig), 0, n, add = TRUE, col = "red")

#TASK 11:
#A~bin(n, p)
n = 100
p = 0.25
#P(A <= 15) = F(15)
print(pbinom(15, n, p))
print(pnorm(15, n*p, sqrt(n*p*(1-p)))) #approximation by normal distribution, pnorm(15, mu, sig)

#TASK 12:
n = 200
size = 30
mn = rep(0,)
for (i in 1:n){
  A = rnorm(size)
  mn[i] = mean(A)
}
hist(mn, freq = F, ylim = c(0, 2.5))
curve(dnorm(x, 0, 1/sqrt(size)), add = T)

#TASK 13:
samples = 200
size = 10
n = 30
p = 0.4
mn = rep(0, 0)
for (i in 0:samples){
  a = rbinom(size, n, p)
  mn[i] = mean(a)
}
hist(mn, freq = F)
mu = n*p
sigma = sqrt(n*p*(1-p))
curve (dnorm(x, mu, sigma/sqrt(size)), add=T, col = "red")

#TASK 14:
mn = 200
sd = 10
size = 50
#R~N(mn, sd)
#Rbar ~ N(mn, sd/sqrt(size))
#a)
pnorm(202, mn, sd/sqrt(size)) - pnorm(199, mn, sd/sqrt(size))
#b)
# T ~ N(mn*size, sd*sqrt(size))
limit = 10020
pnorm(limit, mn*size, sd*sqrt(size))

#TASK 15:
mn = 202
sig=14
sample = 64
#C~?(mu, sig)
#Cbar ~app N(mn, sig/sqrt(sample))
print(paste("Probability that cholesterol is in 198 to 206 is: ", pnorm(206, mn, sig/sqrt(sample)) - pnorm(198, mn, sig/sqrt(sample))))

#if dist is not known and sample is sufficiently big than we will use
#C~ ?(mu, sigma)
#Cbar ~app N(mu, sigma/sqrt(n))

#TASK 16:
mu = 0.5
sig= 0.2
size = 100
weight = 47
#Distribution not known but sample is 47 is enough big to approximate it with normal distribution
#W ~app(mn*size, sig*sqrt(size))
print(paste("Probability that rope will hold 47 lbs is", 1  - pnorm(weight, mu*size, sig*sqrt(size))))

#pnorm(weight, mu*size, sig*sqrt(size)) -> probability that rope will hold less than 47 lbs