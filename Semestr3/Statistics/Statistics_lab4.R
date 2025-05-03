setwd("C:/Users/Kuba/Desktop/Studia/Semestr 3/Statystyka/Laboratories")
data = read.csv("data_est.csv", sep = ";", dec = ".")

#TASK 1:
data
diam = na.omit(data$diamonds) #data frame - $ is for choosing appropriate 
diam
# a)
#Population - all diamonds
# Sample - 12 diamonds
#random variable - weight of synthetic diamond

#b)
mu = mean(diam) #mean of sample
mu

#c)
alpha = 0.05
n = length(diam) #length of sample
S = sd(diam) #sd of sample
from = mu - qt(1 - alpha/2, n-1) * S/sqrt(n)
to = mu + qt(1 - alpha/2, n-1) * S/sqrt(n)
print(paste("We are", (1-alpha)*100, "% confident that interval <", floor(1000*from)/1000, ceiling(1000*to)/1000, "> covers the true meam weight of ALL synthetic diamonds"))

#d)
t.test(diam, conf.level = 1-alpha)
out = t.test(diam) #by the default confidence level is 95%
out$conf.int
#the bigger the confidence level, the bigger must be confidence interval

#e)
var(diam)
S = sd(diam)

#f) now we are testing variance
var_from = (n-1)*S^2/qchisq(1 - alpha/2, n-1)
var_to = (n-1)*S^2/qchisq(alpha/2, n-1)
var_from
var_to

paste("We are", (1 - alpha)*100, "% confident that interval (", floor(sqrt(var_from)*10000)/10000, ",", ceiling(sqrt(var_to)*10000)/10000, ") covers the true sd weight of ALL doiamonds")
sqrt(sigma.test(diam)$conf.int)


#TASK 2
milk <- na.omit(data$milk)
milk

#a)
print("Population - milk of ALL nursing mothers")
print("Sample - milk of 20 nursing moters")
print("Meaurement - amount of PCB in milk")
#b)
milk_bar = mean(milk)

#c)
milk_sd = sd(milk)
milk_var = var(milk)

#d)
alpha = 0.05
n = length(milk)
#testing mean
print(paste("The interval (", floor(100*(milk_bar - qt(1-alpha/2, n-1)*milk_sd/sqrt(n)))/100, ", ", ceiling(100*(milk_bar + qt(1-alpha/2, n-1)*milk_sd/sqrt(n)))/100, ") with 95% covers mean"))

#e)
var_from = (n-1)*milk_sd^2/qchisq(1-alpha/2, n-1)
var_to = (n-1)*milk_sd^2/qchisq(alpha/2, n-1)
print(paste("We are", (1 - alpha)*100, "% confident that interval (", floor(sqrt(var_from)*100)/100, ",", ceiling(sqrt(var_to)*100)/100, ") covers the true sd weight of ALL doiamonds"))
print(paste("We are", (1 - alpha)*100, "% confident that interval (", floor(var_from*100)/100, ",", ceiling(var_to*100)/100, ") covers the true variance weight of ALL doiamonds"))


#TASK 3:
#true sigma is known
#true = regarding all population
cig = na.omit(data$cigarettes)
n=15 #size of sample
alpha = 0.05
sigma = 0.7
xbar = mean(cig)
xbar

#a) Case 1 - known true sigma
lowercig = floor(100*(xbar-qnorm(1-alpha/2)*sigma/sqrt(n)))/100
uppercig = ceiling(100*(xbar+qnorm(1-alpha/2)*sigma/sqrt(n)))/100
print(lowercig)
print(uppercig)
print(paste("We are", 100*(1-alpha), "% sure that interval [", lowercig, uppercig, "] covers true mean of population"))

#b)
#Interval is (Xbar - z * sigma/sqrt(n), Xbar + z*sigma/sqrt(n))
#Length = Xbar + z*sigma/sqrt(n) - (Xbar + z*sigma/sqrt(n)) = 2*z*sigma/sqrt(n)
#Length <= 0.3
#2*z*sigma/sqrt(n) <= 0.3
#0.09 * n >= 4*z^2 * sigma^2
#n >= (4 * z^2 * sigma^2)/0.09
z = qnorm(1 - alpha/2)
n_min = ceiling(4 * z^2 * sigma^2 / 0.09)
print(paste("Minimal sample needed for the length of 95% confidence level to be less or equal to 0.3 is", n_min))

#c)
print(paste("Predicted standard deviation is", round(sd(cig), 2)))
#predicted standard deviation is below true sigma so packs of cigarettes in this sample deviates less from the mean
#than whole population of packs of cigarettes does. Basically packs of cigarettes in this sample were closer to mean
#than all packs normally are


#TASK 4
signal = na.omit(data$signal)
signal
true_sigma = 3 #true sigma
alpha = 0.05
#a) mean
mu_bar = mean(signal) #mean of sample
print(paste("Point estimate of mu is:", mu_bar))

#b) confidence interval
res=z.test(signal, sigma.x = true_sigma, conf.level = 1-alpha) #not obligatory to write - conf.level is by default 95%
int = res$conf.int #first we round down, then up
print(paste("We are ", 100*(1-alpha), "% sure that interval (", floor(100*int[1])/100, "%, ", ceiling(100*int[2])/100, "%) covers point estimate of mu", sep=""))


#TASK 5:
#WE DON'T KNOW THE DISTRIBUTION!!!
#It is large enough so we can estimate it
n = 1200
alpha = 0.05
C_bar = 4.7
S = 2.2
res = zsum.test(C_bar, S, n) #mean
int = res$conf.int
variance_left_endpoint = ((n-1)*(S^2))/qchisq(1 - alpha/2, n - 1)
variance_right_endpoint = ((n-1)*(S^2))/qchisq(alpha/2, n - 1)
left_sd = floor(variance_left_endpoint^(1/2) * 100) / 100
right_sd = ceiling(variance_right_endpoint^(1/2) * 100) / 100
#a) mean
print(paste("We are 95% confident that interval (",floor(100*int[1])/100, ", ", ceiling(100*int[2])/100, ") covers true population mean", sep=""))
#b) sd
print(paste("We are 95% confident that interval (", left_sd, ",", right_sd,") covers true population standard deviation of ALL calls" ))


#TASK 6:
#Distribution not known, true sigma and true mu not known
#sample is large enough (>30) so we can use zsum.test
lifetime = data$lifetime #sample
n = length(lifetime)
alpha = 0.05
L_bar = mean(lifetime)
S = sd(lifetime)
#we use zsum test to find confidence interval
int = zsum.test(L_bar, S, n, conf.level = 1-alpha)$conf.int
print(paste("We are ", 100*(1-alpha), "% sure that mean lifetime of transistor is covered in interval (", floor(int[1]*100)/100, ", ", ceiling(int[2]*100)/100, ")", sep=""))


#TASK 7:
#CASE 1 - known distribution and st dev
var = 25
sd = var^(1/2)
sd
# (Z*sigma)/sqrt(n) <= 1 #error does not exceed 1 hour
# n>= Z^2 * var
alpha = 0.05
n_min = ceiling(qnorm(1 - alpha/2)^2 * var)
n_min
print(paste("If we want to be 95% confident that the error of estimating the mean at most 1 we have a sample size of at least", n_min))


#TASK 8:
#CASE 1 - known distribution and st dev
# (Z*sigma)/sqrt(n) <= error = 0.1 is correct within 0.1 pound == error does not exceed 0.1 pound
# error^2 * n >= Z^2 * var
# n >= Z^2*sig^2/error^2
#Z = qnorm(1 - alpha/2)
sig = 0.3
alpha = 0.1
var = 0.09
error = 0.1
#a)
n_min = ceiling(qnorm(1 - alpha/2)^2 * var/error^2)
n_min
#b)
alpha = 0.01
n_min = ceiling(qnorm(1 - alpha/2)^2 * var/error^2)
n_min


#TASK 9:
#we use all possible methods - the best one is with smallest interval
alpha = 0.05
n = 100
bigt=3
z = qnorm(1 - alpha/2)
z
#own function
p_hat = bigt/n
left_endpoint = max(p_hat - z*sqrt(p_hat*(1-p_hat)/n), 0)
right_endpoint = ceiling(10000*(p_hat + z*sqrt(p_hat*(1-p_hat)/n)))/10000
left_endpoint #left endpoint is <0 so we substitute it with 0 since we can't have negative probability
right_endpoint
print(paste("We are ", 100*(1-alpha), "% sure that true proportion of unscheduled dwontime is in interval (", 0, ", ", 100*right_endpoint, "%)", sep = ""))

#binom test:
int = binom.test(bigt, n)$conf.int
print(paste("We are ", 100*(1-alpha), "% sure that true proportion of unscheduled dwontime is in interval (", floor(10000*int[1])/100, "%, ", ceiling(10000*int[2])/100, "%)", sep = ""))

#prop test:
int = prop.test(bigt, n)$conf.int
print(paste("We are ", 100*(1-alpha), "% sure that true proportion of unscheduled dwontime is in interval (", floor(10000*int[1])/100, "%, ", ceiling(10000*int[2])/100, "%)", sep = ""))


#TASK 10:
n = 100
bigt = 4
alpha = 0.05
p_hat = bigt/n
#sample is >=100 so we are allowed to approximate this distribution with normal dist
z=qnorm(1 - alpha/2)
left_endpoint = floor(10000*(p_hat - z*sqrt(p_hat*(1-p_hat)/n)))/100
right_endpoint = ceiling(10000*(p_hat + z*sqrt(p_hat*(1-p_hat)/n)))/100
print(paste("We are ", 100*(1-alpha), "% sure that true proportion is covered in interval (", left_endpoint, "%, ", right_endpoint, "%)", sep=""))


#TASK 11:
bigt = 24
n = 120
p_hat = bigt/n
alpha = 0.1
z = qnorm(1 - alpha/2)
left_endpoint = floor(10000*(p_hat - z*sqrt(p_hat*(1- p_hat)/n)))/100
right_endpoint = ceiling(10000*(p_hat + z*sqrt(p_hat*(1- p_hat)/n)))/100
print(paste("We are ", 100*(1-alpha),"% confident that interval (", left_endpoint, "%, ", right_endpoint, "%) covers true proportion", sep=""))


#TASK 12:
n = 1000
bigt = 122
p_hat = bigt/n
alpha = 0.1
z=qnorm(1 - alpha/2)
left_endpoint = floor(10000*(p_hat - z*sqrt(p_hat*(1-p_hat)/n)))/100
right_endpoint = ceiling(10000*(p_hat + z*sqrt(p_hat*(1-p_hat)/n)))/100
left_endpoint
right_endpoint
print(paste("We are ", 100*(1-alpha), "% sure that interval (", left_endpoint, "%, ", right_endpoint, "%) covers true proportion"))


#TASK 13:
alpha = 0.02
#(z*sqrt(phat*(1-phat)/n)) <= 0.05
#about we use round, else ceiling or floor
#a)
#if proportion is unknown we assume it is equal 0.5 (fifty - fifty)
z = qnorm(1 - alpha/2)
phat = 0.5
n_min1= ceiling(20^2 * z^2 * phat*(1 - phat))
print(paste("If we know nothing about proportion, then we should examine:", n_min1, "people"))
#b)
phat = 0.3
n_min2= ceiling(20^2 * z^2 * phat*(1 - phat))
print(paste("If we know proportion is 0.3 then we should examine:", n_min2, "people"))

#ztest - distribution and sigma known -> for mean (mu)
#zsum - sample is large (very important), distribution is not known -> for mean(mu)
#t test - sigma unknown -> for mean (mu)
#sigma.test -> test for variance

#sample -> people asked (people asked in exit poll)
#population -> all people (all voters)
#for big enough sample mean, sd etc are very close to mean, sd etc of all (true) population (for 75 k of voters exit poll was very close to reality)