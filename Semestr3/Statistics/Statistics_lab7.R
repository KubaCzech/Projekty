setwd("C:/Users/Kuba/Desktop/Studia/Semestr 3/Statystyka/Laboratories")

#TASK 1:
data = read.csv("Anova_pressure.csv", sep = ";")
data
alpha = 0.05
results = c(data$Low, data$Moderate, data$Strong, data$VeryStrong)

n = length(data$Low)
n
N = 4*n #number of all, each column has 10 values, there are 4 columns
treatments = rep(names(data), each = n)
treatments

#1. TESTING VARIANCES - neccessary condition to go on
#H0: variances are equal

res = bartlett.test(results ~ treatments)
res

#p.value > 0.05 => no reason to reject H0
#that is, assume variances are equal
ts = rep(0, 0)
ts[1] = sum(data$Low)
ts[2] = sum(data$Moderate)
ts[3] = sum(data$Strong)
ts[4] = sum(data$VeryStrong)
t_total = sum(ts)
t_total

sst = sum(ts^2)/n  - (t_total^2)/(N)
sst

ssg = sum(data^2) - t_total^2 /(N)
ssg

sse = ssg - sst
sse

k = length(names(data))
mst = sst/(k-1)
mst
mse = sse/(N-k)
mse

#Second method with all results
anova(lm(results~treatments))

#p.value > 0.05 => no reason to reject H0

#TASK 3:
data = read.csv("Anova_micrometer.csv", sep = ";")
n = rep(0, 0)
for (i in 1:3){
  n[i] = length(na.omit(data[, i]))
}

results = c(na.omit(data$micro1), na.omit(data$micro2), na.omit(data$micro3))
treatments = rep(names(data), n)

#STEP 1: check variances
#H0: variances are equal
bartlett.test(results~treatments)
#alpha < p-value -> no reason to reject H0

anova(lm(results~treatments))

#TASK 4:
data = read.csv("Anova_traps.csv", sep=";")
n = length(data$scattered)
N = n*length(names(data))

results = c(data$scattered, data$concentrated, data$host.plant, data$aerial, data$ground)
treatments = rep(names(data), each = n)

#We check null hypothesis -> H0: variances are equal
bartlett.test(results~treatments)
alpha = 0.05
#p-val = 0.06 > alpha = 0.05 => no reason to reject H0

anova(lm(results~treatments))
#alpha > Pr(>F)
#b)
TukeyHSD(aov(results~treatments), ordered = T)

#TASK 5:
data = read.csv("Anova_sportsmen.csv", sep = ";")
data

alpha = 0.05

#STEP 1: verify homogenity of variances
#H0: variances are equal
results = c(data$NonSmokers, data$LightSmokers, data$MediumSmokers, data$HeavySmokers)

n = length(data$NonSmokers)
n
N = 4*n #number of all, each column has 10 values, there are 4 columns
treatments = rep(names, each = n)
treatments

res = bartlett.test(results ~ treatments)
res
#alpha < p-value -> no reason to reject H0
#we can perform ANOVA

#STEP 2: check everything else
#H0: there is no significant influence
#HA: there is significant difference in mean
res1 = anova(lm(results~treatments))
res1$`Pr(>F)`[1]
#alpha > p-value -> we reject H0
#Thus there is significant difference

#b)
TukeyHSD(aov(results~treatments), ordered = T)
#First group: (N, M, H), 
#Second group: (L, H)