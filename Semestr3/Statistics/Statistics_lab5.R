#Null hypothesis == sth we want to prove false (we are ensuring that H0 is false, so HA must hold), 
#alternative hypothesis == negation of null hypothesis. In other words HA is something we want to be true

setwd("C:/Users/Kuba/Desktop/Studia/Semestr 3/Statystyka/Laboratories")
data = read.csv("data_hip.csv", sep = ";")
head(data)
library("arm")
library("BSDA")
library("TeachingDemos")

#TASK 1: mu - case 3
#H0: mu <= 4 -> VERY IMPORTANT
#H1: mu > 4 (H1 == HA, where A == alternative) -> VERY IMPORTANT
#Xbar == mean of sample
#S == sd of sample
#mu0 = 4
#n == size of sample

wind = na.omit(data$wind)
wind

alpha = 0.05
Xbar = mean(wind)
S = sd(wind)
mu0 = 4
n = length(wind)

t = (Xbar - mu0) * sqrt(n)/S
qt(1 - alpha, n - 1)
t
print(paste("Reject H0")) #t is in the critical region
# we reject the null hypothesis
#if t in critical region, then we reject H0

#Second method
library("BSDA")
res = t.test(wind, mu = mu0, alternative = "greater")
res$p.value
#p-value: turning point from which we reject or not H0, if p < alpha -> we reject null hypothesis

#TASK 2: mu - case 3
#H0: mu >= 3.5
#H1: mu < 3.5
#X - random variable denoting COP

indices = na.omit(data$COP)
indices

alpha = 0.01
Xbar = mean(indices)
S = sd(indices)
mu0 = 3.5
n = length(indices)

t = (Xbar - mu0) * sqrt(n)/S
qt(1 - alpha, n - 1)
t
#R = (-Inf, -2.821)
if (t < -qt(1 - alpha, n-1)){
  print("Reject H0")
}else{
  print("No reason to reject H0")
}

#second method:
res = t.test(indices, mu = mu0, alternative = "less")$p.value
res < alpha
#FALSE - we do not reject H0

p_value = pt(t, n-1) # == p-value
p_value

#TASK 3: mu - case 1
#H0: mu = mu0
#H1: mu != mu0
#Distribution is normal, true sigma known

systems = na.omit(data$temperature)
systems
alpha = 0.01

Xbar = mean(systems)
n = length(systems)
sigma = 2
mu0 = 54

z = (Xbar - mu0)*sqrt(n)/sigma
z

qn = qnorm(1 - alpha/2)
#R = (-Inf, -qn) U (qn, Inf)
#R = (-Inf, -2.576) U (2.576, Inf) -> z not in R
print("No reason to reject H0")

#Second method
res = z.test(systems, sigma.x = sigma, mu = mu0, alternative = "two.sided")$p.value
res
res < alpha
#FALSE -> no reason to reject H0

#TASK 4: mu0 - case 1
#H0: mu= mu0
#H1: mu != mu0

depths = na.omit(data$depth)
depths

alpha = 0.05
mu0 = 870
Xbar = mean(depths)
sig = 5
n = length(depths)

z = (Xbar - mu0)* sqrt(n)/sig
z

qn = qnorm(1 - alpha/2)
qn

#R = (-Inf, -1.96) U (1.96, Inf) -> z not in R
print("There is no reason to reject H0")

#Second method
res = z.test(depths, sigma.x = sig, mu = mu0, alternative = "two.sided")$p.value
res
res < alpha
print("There is no reason to reject H0")

#TASK 5: mu - case 2, we dont know distribution but sample is large enough to assume normality
#H0: mu >= mu0
#H1: mu < mu0

thick = na.omit(data$thickness)
thick

alpha = 0.05
mu0 = 0.04
Xbar = mean(thick)
S = sd(thick)
n = length(thick)

z = (Xbar - mu0)*sqrt(n)/S
z

zb = qnorm(1 - alpha)
zb

#R = (-Inf, -1.645) U (1.645, Inf) -> z in R, we reject R0
print("We reject H0")

#Second method
res = zsum.test(Xbar, S, n, mu = mu0, alternative = "less")$p.value
res
res < alpha #TRUE -> we reject H0

#TASK 6:
#a) case 3 - true sigma not known, normality
#H0: mu = 16
#H1: mu != 16
eggs = na.omit(data$length)
mu0 = 16
alpha = 0.05
n = 21
Xbar = mean(eggs)
S = sd(eggs)

t = sqrt(n) * (Xbar - mu0)/S
qt(1 - alpha/2, n-1)
#Critical region R = (-Inf, -2.086) U (2.086, Inf)
#t in R -> reject H0

res = t.test(eggs, mu = mu0, alternative = "two.sided")
res$p.value
#p-value = 0 < alpha -> reject H0

#b)
#H0: mu = 3
#H1: mu != 3
sig0 = 3
chsq = ((n-1)* S^2)/sig0^2
chsq

qchisq(alpha/2, n-1)
qchisq(1-alpha/2, n-1)
#Critical region R = (0, 9.591) U (34.17, Inf)
#chsq not in R -> no reason to reject H0

res = sigma.test(eggs, sigmasq = sig0^2, alternative = "two.sided")
res$p.value
#p-value = 0.09 > alpha -> reject H0

#TASK 7:
fat = na.omit(data$fat)
fat
alpha = 0.05
n = length(fat)
#a) case 3 - normality, true sigma not known
#H0: mu = mu0
#H1: mu != mu0
mu0 = 1.7
Xbar = mean(fat)
S = sd(fat)
t = (Xbar - mu0)*sqrt(n)/S
t
qt(1-alpha/2, n-1)
#Critical region R = (-Inf, -2.262) U (2.262, Inf)
#t not in R -> no reason to reject H0

res = t.test(fat, mu = mu0, alternative = "two.sided")
res$p.value
#p-value = 0.11 > alpha, no reason to reject H0

#b) Now we test variance; 
#H0: var >= var0
#H1: var < var0
var0 = 0.02
xsq = (n-1)*S^2/ var0
xsq

upper = qchisq(alpha, n-1)
upper
#Critical region R = (0, 3.325)
#xsq not in R
print("There is no reason to reject H0")

res = sigma.test(fat, sigmasq = var0, alternative = "less")
res$p.value

#TASK 8:
alpha = 0.01
n = 100
S = 20
Xbar = 60
#About mean - case 2 -> distribution not known, large enough sample
#H0: mu <= mu0
#H1: mu > mu0
mu0 = 55
z = (Xbar - mu0) * sqrt(n)/S
z

zb = qnorm(1 - alpha)
zb
#Critical region R = (2.326, Inf)
#z in R -> reject H0

res = zsum.test(Xbar, S, n, mu = mu0, alternative = "greater") #greater/less gdy hipotez to > albo <, two.sided gdy !=
res$p.value

#About sd
#H0: sigma <= sigma0
#H1: sigma > sigma0
sig0 = 18
xsq = (n-1)*S^2/sig0^2
xsq

qchisq(1-alpha, n-1)
#Critical region R = (134.6416, Inf)
#xsq not in R -> no reason to reject H0

#TASK 9:
#H0: p <= 0.9 
#H1: p > 0.9 the part we want to check is alternative 

alpha = 0.05
bigt = 1000
n = 1100
p_hat = bigt/n
p0 = 0.9

Z = (p_hat - p0)*sqrt(n) / sqrt(p0*(1 - p0))
Z

q1 = qnorm(1-alpha)
q1
#Critical region: (1.645, Inf)
#test statistic not in the interval
#there is no reason to reject H0

binom.test(1000, 1100, p = p0, alternative = "greater")$p.value

prop.test(1000, 1100, p = p0, alternative = "greater")$p.value

#TASK 10:
#H0: p = p0
#H1: p != p0
n = 150
bigt = 82
p_hat = bigt/n
p0 = 0.4
alpha = 0.01
z = (p_hat - p0)*sqrt(n)/sqrt(p0*(1-p0))
z

qnorm(1-alpha/2) #2.575

#Critical region R = (-Inf, -2.575) U (2.575, Inf)
#z in R -> reject H0
#Data confirms that true population proportion differs from 40% of blood type A

binom.test(bigt, n, p=p0, alternative = "two.sided")$p.value
#p-value < alpha -> reject H0

prop.test(bigt, n, p = p0, alternative = "two.sided")$p.value
#p-value < alpha -> reject H0

#Task 11:
#H0: p <= p0
#H1: p > p0

n = 91
bigt = 16
p_hat = bigt/n
p0 = 0.15
alpha = 0.1

z = (p_hat - p0)*sqrt(n)/sqrt(p0*(1-p0))
z

qnorm(1-alpha)

#Critical region R = (1.282, Inf)
#z not in R -> no reason to reject H0