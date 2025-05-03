#156035
#Kuba Czech

setwd("C:/Users/Kuba/Desktop/Studia/Semestr 3/Statystyka/Laboratories")
data = read.csv("dataTest2.csv", sep = ";", dec = ",")

#TASK 1:
pop = na.omit(data$lenght)
pop
n = length(pop)
n
alpha = 0.05

#H0: mu >= mu0
#HA: mu < mu0
#mu0 = 4

Xbar = mean(pop)
mu0 = 4
S = sd(pop)

z = (Xbar - mu0)/(S/sqrt(n))
z

q = qnorm(1 - alpha)
q

#Critical region R: (-Inf, -1.645) -> z not in R
#There is no reason to reject H0
#So we can't confirm clients suspicions

#TASK 2:
#we can use formulas because 105 > 100
#H0: p <= p0
#HA: p > p0
bigT = 51
n = 105
p0 = 0.5
alpha = 0.1

p_hat = bigT/n

z = sqrt(n)*(p_hat - p0)/sqrt(p0*(1-p0))
z

q = qnorm(1-alpha)
q

#Critical region R: (1.282, Inf) -> z not in R
#There is no reason to reject H0
#We can't confirm suspicions

res1 = binom.test(bigT, n, p = p0, alternative = "greater")
res1$p.value

res2 = prop.test(bigT, n, p = p0, alternative = "greater")
res2$p.value

#In both cases p-value > alpha -> no reason to reject H0
#We can't confirm suspicions

#TASK 3:
before = na.omit(data$before)
after = na.omit(data$after)

diff = before - after
diff
alpha = 0.05

#a)
Xbar = mean(diff)
Xbar
S = sd(diff)
S
#We are testing hypothesis:
#H0: mu = 0
#H1: mu != 0
mu0 = 0
t = (Xbar - mu0)/(S/sqrt(length(diff)))
t #4.453

q = qt(1-alpha/2, length(diff) - 1)
q #2.20

#Critical region R: (-Inf, -2.20) U (2.20, Inf) -> t in R
#We reject H0
#We can confirm doctor's suspicions

#b)
res = t.test(diff, mu = 0, alternative = "two.sided", conf.level = 0.95)$conf.int
res
#confidence interval: (2.149, 6.351)
#We know with 95% significance level that mean difference of chemical parameter before and after taking medicine is in this interval
#Since interval is positive, difference is positive and we see that we can confirm doctor's suspicions 

#TASK 4:
pop1 = na.omit(data$bus)
pop2 = na.omit(data$tram)

alpha = 0.1

n1 = length(pop1)
n2 = length(pop2)

#STEP 1: testing variances
#H0: var1 == var2
#HA: var1 != var2
s1 = sd(pop1)
s2 = sd(pop2)

FF = s1^2 / s2^2
FF #3.25
q1 = qf(alpha/2, n1 - 1, n2 - 1)
q2 = qf(1 - alpha/2, n1 - 1, n2 - 1)
q1 #0.35
q2 #2.943

#Crititcal region (0, 0.35) U (2.943, Inf)
#we reject H0
#varainces are not equal!!!

#STEP 2: checking means
#H0: mu1 - mu2 <= 0
#HA: mu1 - mu2 > 0
res = t.test(pop1, pop2, var.equal = FALSE, mu = 0, alternative = "greater")
res$p.value
#We reject H0
#p-val < alpha
#we can confirm resident's suspicions

#TASK 5:
length(na.omit(data$wheat1))
length(na.omit(data$wheat2))
length(na.omit(data$wheat3))
length(na.omit(data$wheat4))
length(na.omit(data$wheat5))
#all populations have equal sizes - important

alpha = 0.05

#STEP 1: verify homogenity (or how is this called)
#H0: variances are equal
#HA: variances are not equal
results = c(na.omit(data$wheat1), na.omit(data$wheat2), na.omit(data$wheat3), na.omit(data$wheat4), na.omit(data$wheat5))

n = length(na.omit(data$wheat1))
n
N = 5*n #number of all, each column has 11 values, there are 5 columns
someNames = c("wheat1", "wheat2", "wheat3", "wheat4", "wheat5")
treatments = rep(someNames, each = 11)
treatments

res = bartlett.test(results ~ treatments)
res
#alpha < p-value -> no reason to reject H0
#we can perform ANOVA

#STEP 2: check everything else
#H0: there is no significant influence
#HA: there is significant difference of means
res1 = anova(lm(results~treatments))
res1$`Pr(>F)`[1]
#alpha > p-value -> we reject H0
#Thus there is significant difference

TukeyHSD(aov(results~treatments), ordered = T)
#First group: (W2, W4), W1 -> wheat 1
#Second group: (W1, W3, W5)

#TASK 6:
x = na.omit(data$weight)
y = na.omit(data$cholesterol)

#a)
cov(x, y)

#b)
cor(x, y) #Very strong correlation

#c)
plot(x, y)

#d)
line = lm(y~x)
abline(line, col = "red")
line #y_hat = 23.05 + 2.233x

#e)
round(predict(line, data.frame(x = 90))) #it will be 224

#f)
round(predict(line, data.frame(x = 105))) #it will be 257

#g)
summary(line)
#p.value = 0
#alpha > p.value
#Interpretation: approximation by this model is good

#TASK 7:
xx = na.omit(data$time)
yy = na.omit(data$temperature)

rm(x)

#a)
plot(xx, yy)
#order 2
model2 = lm(yy~xx+I(xx^2))
summary(model2)
coefs2 = model2$coefficients
curve(coefs2[1] + coefs2[2]*x + coefs2[3]*x^2, add = T, col = "red")

plot(xx, yy)
#order 3
model3 = lm(yy~xx+I(xx^2)+I(xx^3))
summary(model3)
coefs3 = model3$coefficients
curve(coefs3[1] + coefs3[2]*x + coefs3[3]*x^2 + coefs3[4]*x^3, add = T, col = "red")

plot(xx, yy)
#order 4
model4 = lm(yy~xx+I(xx^2)+I(xx^3)+I(xx^4))
summary(model4)
coefs4 = model4$coefficients
curve(coefs4[1] + coefs4[2]*x + coefs4[3]*x^2 + coefs4[4]*x^3 + coefs4[5]*x^4, add = T, col = "red")

#b)
summary(model2) #38.5%
summary(model3) #41.9%
summary(model4) #83.3%

#c)
summary(model4)
#p.value = 0.016
#p.value < alpha
#model is good

#d)
round(predict(model4, data.frame(xx = 328/60))) #52 5h 28 min == 328/60 h
