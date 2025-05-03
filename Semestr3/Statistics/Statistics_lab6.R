setwd("C:/Users/Kuba/Desktop/Studia/Semestr 3/Statystyka/Laboratories")

library("Paired Data")

data = read.csv("data_twoPop.csv", sep = ";")

#TASK 1:
pop1 = na.omit(data$cellulose1)
pop2 = na.omit(data$cellulose2)

n1 = length(pop1)
n2 = length(pop2)

alpha = 0.02

Xbar = mean(pop1)
Ybar = mean(pop2)

#a)
#H0: var1 == var2
#HA: var1 != var2
s1 = sd(pop1)
s2 = sd(pop2)

FF = s1^2 / s2^2 #0.479
q1 = qf(alpha/2, n1 - 1, n2 - 1)
q2 = qf(1 - alpha/2, n1 - 1, n2 - 1)
q1 #0.162
q2 #3.699

#Crititcal region (0, 0.162) U (3.699, Inf)
#FF not in R -> no reason to reject H0

#b)
#H0: mu1 - mu2 == 0
#HA: mu1 - mu2 != 0
res = t.test(pop1, pop2, var.equal = TRUE, mu = 0, alternative = "two.sided")
res$p.value
#No reason to reject H0
#p-val > alpha

#c)
Sp2 = ((n1 -1) * s1^2 + (n2 - 1)*s2^2)/(n1 + n2 - 2)
error = qt(1 - alpha/2, n1+n2 - 2)*sqrt(Sp2 * (1/n1 + 1/n2))
upper = Xbar - Ybar + error
lower = Xbar - Ybar - error
upper
lower
#The interval that covers mu -> (-13.52, 3.144)

#TASK 2:
alpha = .1
house1 = na.omit(data$traditional)
house2 = na.omit(data$new)

n1 = length(house1)
n2 = length(house2)
n1
n2

Xbar = mean(house1)
Ybar = mean(house2)
S1 = sd(house1)
S2 = sd(house2)

#STEP 1: checking variances
#H0: var1 == var2
#HA: var1 != var2
res = var.test(house1, house2, conf.level = 1 - alpha)
res$p.value
#alpha < p.value
#No reason to reject H0

#STEP 2: checking means
#H0: mu1 >= mu2
#HA: mu1 < mu2
Sp2 = ((n1 - 1)*S1^2 + (n2 - 1)*S2^2 )/(n2 + n1 - 2)
t = (Xbar - Ybar) / sqrt(Sp2 * (1/n1 + 1/n2))
t
right = qt(1 - alpha, n1+n2 -2)
right
#Critical region R = (-Inf, -1.327) -> alpha not in R
#There is no reason to reject H0

#TASK 3:
alpha = 0.1
#Step 1 - checking variances !!!
#H0: var1 == var2
#H1: var1 != var2
loans1 = na.omit(data$public)
loans2 = na.omit(data$private)

n1 = length(loans1)
n2 = length(loans2)

n1
n2
var.test(loans1, loans2, conf.level = 1-alpha)
#p-value == 0.08687
#We reject H0 -> variances are significantly different

#Step 2 - testing means
#H0: mu1 >= mu2
#H1: mu1 < mu2
mu0 = 0
res = t.test(loans1, loans2, var.equal = FALSE, mu = mu0, alternative = "less")
res$p.value
#p-value = 0.023 < alpha
#We reject H0

#TASK 4:
player1 = na.omit(data$player1)
player2 = na.omit(data$player2)
n1 = length(player1)
n2 = length(player2)

alpha = 0.05

#Step 1 - checking variances
#H0: var1 >= var2
#H1: var1 < var2
var.test(player1, player2, alternative = "less")
#p-value = 0.211 > alpha = alpha -> no reason to reject H0
#player 1 does not have more stable results

#TASK 5:
pop1 = na.omit(data$medicine1)
pop2 = na.omit(data$medicine2)
n1 = length(pop1)
n2 = length(pop2)

Xbar = mean(pop1)
Ybar = mean(pop2)
S1 = sd(pop1)
S2 = sd(pop2)

alpha = 0.1


#STEP 1: check variances
#H0: var1 == var2
#HA: var1 != var2
res = var.test(pop1, pop2, conf.level = 1-alpha)$p.value
res
#p.value > alpha -> no reason to reject H0

#STEP 2: check means
#H0: mu1 <= mu2
#HA: mu1 > mu2
Sp2 = ((n1 - 1)*S1^2 + (n2 - 1)*S2^2 )/(n2 + n1 - 2)
t = (Xbar - Ybar)/ sqrt(Sp2 * (1/n1 + 1/n2))
t

qt(1-alpha, n1+n2 - 2)

#Critical region R = (1.319, Inf) -> t in R
#We reject H0

#TASK 6:
n1 = 1200
n2 = 2000
p1 = 0.78
p2 = 0.8
T1 = n1*p1
T2 = n2*p2
alpha = 0.1
p_hat = (T1 + T2)/(n1 + n2)

#a)
error = qnorm(1 - alpha/2) * sqrt(p1*(1 - p1)/n1 + p2*(1 - p2)/n2)
lower = p1 - p2 - error
upper = p1 - p2 + error

lower
upper
#Confidence interval covering true difference between Poles and Americans: (-4.46%, 0.46%)

res = prop.test(c(T1, T2), c(n1, n2), conf.level = 1 - alpha)
res$conf.int
#confidence interval: (-4.53%, 0.53%)

#b)
z = (p1 - p2) / sqrt(p_hat * (1 - p_hat) * (1/n1 + 1/n2))
z # -1.351

#H0: p1 == p2
#HA: p1 != p2
q = qnorm(1 - alpha/2)
q

#Critical region R:
#(-Inf, -1.645) U (1.645, Inf)
#Test statistic value not in critical region
#no reason to reject H0

#TASK 7:
T1 = 313
T2 = 145
n1 = 313+28
n2 = 145+56
p1 = T1/n1
p2 = T2/n2
alpha = 0.05

p_hat = (T1 + T2)/(n1 + n2)

#a)
#H0: p1 == p2
#HA: p1 != p2

z = (p1 - p2)/sqrt(p_hat*(1 - p_hat) *(1/n1 + 1/n2))
z

q = qnorm(1 - alpha/2)
q

#Critical region: (-Inf, -1.96) U (1.96, Inf) -> z in critical region
#we reject H0
#malaria of type A depends on region

#b)
error = q*sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
lower = p1 - p2 - error
upper = p1 - p2 + error

lower
upper
#Confidence interval: (12.8%, 26,5%) covers true difference with 95% significance, so type A of malaria depends on region

#TASK 8:
#H0: p1 >= p2
#HA: p1 < p2
T1 = 47
T2 = 62
n = 1000
p1 = T1/n
p2 = T2/n
p_hat = (T1 + T2)/(2*n)
alpha = 0.05

z = (p1 - p2)/sqrt(p_hat*(1-p_hat)*(2/n))
z

q = qnorm(1 - alpha/2)
q

#Critical region R: (-Inf, -1.96)
#z not in R -> no reason to reject H0
#He should choose design B


#TASK 9 -> out of two sets of data we compute the difference and use t.test:
#Data normally distributed, true sigma not known -> case 3
before = na.omit(data$drugBefore)
after = na.omit(data$drugAfter)
diff = before - after
diff
alpha = 0.05

Xbar = mean(diff)
Xbar
S = sd(diff)
S
#We are testing hypothesis:
#H0: mu = 0
#H1: mu != 0
res = t.test(diff, mu = 0, alternative = "two.sided")
res$p.value

#p.value is greater than significance level so there is no reason to reject H0
#We cannot confirm doctor's suspicions

t = Xbar/(S/sqrt(length(diff)))
t

q = qt(1-alpha/2, length(diff) - 1)
q
#Critical region R: (-Inf, -2.31) U (2.31, Inf) -> t not in R
#No reason to reject H0
#We cannot confirm doctor's suspicions

#TASK 10:
shallow = na.omit(data$pH15)
deep = na.omit(data$pH100)
alpha = 0.1

Xbar = mean(diff)
Xbar
S = sd(diff)
S

#a)
diff = deep - shallow
diff

#H0: mu = 0, H1: mu != 0
#one method:
t.test(diff, mu = 0, alternative = "two.sided")$p.value
#0.23 > 0.1 -> p.value > significance level
#The data does not confirm that the pH of the water depend on depth

#second method:
t = Xbar/(S/sqrt(length(diff)))
t

q = qt(1-alpha/2, length(diff) - 1)
q

#Critical region R: (-Inf, -1.89) U (1.89, Inf) -> t not in R
#No reason to reject H0
#We cannot confirm suspicions

#b)
t.test(diff, mu = 0, alternative = "two.sided", conf.level = 0.9)$conf.int
#pH does not depend on depth, because the difference can be either positive or negative
