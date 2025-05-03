#Kuba Czech
#156035
#Group 1

setwd("C:/Users/Kuba/Desktop")
data = na.omit(read.csv("IrisSepalLength.csv", sep = ";", dec = ","))
data

library("arm")
library("BSDA")
library("TeachingDemos")

#TASK 1:
names = colnames(data)
names
n = length(names)
n
#a)
for (i in 1:n){
  print(paste("For", names[i]))
  print(paste("Mean is:", round(mean(data[, i]), 2), "- average of the set"))
  print(paste("Quartile 0 (min):", min(data[, i]), "- smallest value")) #0 quartile
  print(paste("Quartile 1 - at least 25% is smaller or equal, at least 75% are greater or equal to:", quantile(data[, i])[2])) #25% element
  print(paste("Quartile 2 (median):", quantile(data[, i])[3], "- it means that this is the middle element - at least half is greater or equal and at least half is smaller or equal")) #third quantile is median; however quantile != quartile (always quarters)
  print(paste("Quartile 3 - at least 75% of elements are smaller or equal, at least 25% are greater or equal to:", quantile(data[, i])[4])) #75% element
  print(paste("Quartile 4: (max):", max(data[, i]), "- biggest value")) #fourth quartile
  print(paste("Standard deviation is:", round(sd(data[,i]), 2), "- on average this much the elements deviates from the mean"))
  print(paste("Variability index is:", round(100*sd(data[,i])/mean(data[, i]), 2)))
  print(" ")
}
#b)
par(mfrow = c(1, 3))
for (i in 1:n){
  hist(data[, i], main = names[i], xlab = "Length of Iris", ylab = "Frequency of occurence of a value", ylim = c(0, 20), col = i)
}

#c)
par(mfrow = c(1, 1))
boxplot(data[, 1], data[, 2], data[, 3], col = c("red", "green", "blue"), main = "Comparison of length different species of Iris", ylab = "Length", xlab = "Setosa, Versicolor, Virginica")
#black line - median, upper bound of box - third quartile, lowe bound of grey box - first quartile, dot - outlier

#TASK 2:
p = 0.2
n = 9
x = 0:n
#A - random variable (number of cars meeting the condition)
#A~bin(n, p)
cars = dbinom(x, n, p)
cars
#a) i)
print(paste("Exactly 4 cars have a mouldy air conditioning", cars[x == 4]))
#ii)
print(paste("At least 5 cars have a mouldy air conditioning", sum(cars[x >=5])))
#iii)
print(paste("Less than 3 cars have a mouldy air conditioning", sum(cars[x < 3])))

#b)
print(paste("Expected value is:", n*p))

#c)
print(paste("standard dev is:", sqrt(n*p*(1-p))))

#TASK 3:
#R - random variable, number of damadged rollers
#R~exp(1/4.3)
rm(x)
mn = 4.3
lambda = 1/mn
#a)
curve(dexp(x, lambda), 0, 25)
#b)
#i) P(R> 10) = 1 - F(10)
print(paste("number of damadged roller eceed 10", round(1- pexp(10, lambda), 4)))
#ii) P(5<R<8) = F(8) - F(5)
print(paste("number of damadged roller eceed 10", round(pexp(8, lambda) - pexp(5, lambda), 4)))
#iii)
f = function(x){lambda * exp(-1*lambda * x)}
#Veryfying i)
integrate(f, 10, Inf)
#Veryfying ii)
integrate(f, 5, 8)

#TASK 4:
mu = 5 #true mean
sigma = 2 #true sd
#D - random variable, delay of the train
#D~N(mu, sigma)
#a) 
n = 40
#i)
print(paste("Probability that average train delay in (4.8, 5.1):", round(pnorm(5.1, mu, sigma/sqrt(n)) - pnorm(4.8, mu, sigma/sqrt(n)), 4)))
#ii)
#3h == 180 min
print(paste("Probability that total is more than 3h is:", round(1 - (pnorm(180, mu*n, sigma*sqrt(n))), 3)))

#b)
mn = rep(0,)
summ = rep(0,)
for (i in 1:200){
  a = rnorm(n, mu, sigma)
  mn[i] = mean(a)
  summ[i] = sum(a)
}
#i)
hist(mn, freq = F, ylim = c(0, 1.5), col = "blue", xlab = "mean of elements")
curve(dnorm(x, mu, sigma/sqrt(n)), add = T, col = "red")

#ii)
hist(summ, freq = F, col = "blue", ylim = c(0, 0.035), xlab = "sum of elements")
curve(dnorm(x, mu*n, sigma*sqrt(n)), add = T, col = "red")

#TASK 5:
concrete = c(25, 23, 28, 25, 27, 31, 26, 27, 29, 22, 24, 30, 29, 24, 25)
n = length(concrete)
#a)
#Population - all quick-drying concretes
#Sample - 15 chosen quick-drying concretes
#Measurement - time of drying

#b)
alpha = 0.05
C_bar = mean(concrete)
S = sd(concrete)
#true mean and true sigma not known, normal distribution -> Case 2
int = zsum.test(C_bar, S, n, conf.level = 1-alpha)$conf.int
int
print(paste("We are", (1-alpha)*100, "% sure that interval (", floor(1000*int[1])/1000, ",", ceiling(1000*int[2])/1000, ") covers the true mean of population"))

#c)
alpha = 0.04
left_var_endpoint = (n-1)*S^2/qchisq(1 - alpha/2, n-1)
right_var_endpoint = (n-1)*S^2/qchisq(alpha/2, n-1)
left_var_endpoint
right_var_endpoint
print(paste("We are", (1-alpha)*100, "% sure that interval (", floor(1000*sqrt(left_var_endpoint))/1000, ",", ceiling(1000*sqrt(right_var_endpoint))/1000, ") covers the true standard deviation of population"))


#TASK 6:
n = 1000
bigt = 130
p_hat = bigt/n
#a)
print(paste("Estimated proportion of drivers unable to work is: ", 100*(p_hat), "%", sep = ""))

#b)
alpha = 0.1
z = qnorm(1 - alpha/2)
left_end = floor(10000*(p_hat - z*sqrt(p_hat*(1 - p_hat)/n)))/ 100
right_end = ceiling(10000*(p_hat + z*sqrt(p_hat*(1 - p_hat)/n)))/ 100
print(paste("We are", 100*(1 - alpha), "% confident that interval (", left_end, "%,", right_end, "%) covers true proportion of all drivers unable to work"))

#c)
alpha = 0.05
error = 0.04
#z*sqrt(p_hat*(1 - p_hat)/ n) <= error = 0.04
#n >= z^2 * p_hat *(1-p_hat)/error^2
z = qnorm(1 - alpha/2)
n = ceiling(25^2 * z^2 * p_hat*(1 - p_hat)) #we need to round it up, 25 == 1/0.04
print(paste("To obtain estimation error == 0.04 on confidence level = 95% we need to examine at least", n, "people"))
