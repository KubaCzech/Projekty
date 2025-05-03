setwd("/Users/Kuba/Desktop/Studia/Semestr 3/Statystyka/Laboratories")

#TASK 1:
data = read.csv("Reg_1_materials_yield.csv", sep = ";")

x = data$X
y = data$Y

#a)
cov(x, y)

#b)
cor(x, y)

#c)
plot(x, y, pch = 18)
#line correlation is visible

#d)
line = lm(y~x)
line
abline(line, col = "red")

#e) 
#y = 3.62x + 22.41
#it will change by 3.62 -> linear function

#f)
print(3.62 * 15 + 22.41)
prediction = predict(line, data.frame(x = 15)) #x = number for which we need to predict
print(round(prediction, 0))

#g)
print(3.62 * 20 + 22.41)
prediction = predict(line, data.frame(x = 20)) #x = number for which we need to predict
print(round(prediction, 0))

#h)
summary(line) #80% is quality of model

#i)
result = anova(line)
pval = result$`Pr(>F)`[1]
pval
alpha = 0.05

#H0: b == 0, HA: b != 0
#regression coefficient == slope

if(pval < alpha){
  print("Reject H0")
}else{
  print("No reason to reject H0")
}

#H0 is rejected => b!=0

#TASK 2:
arsenic = read.csv("Reg_2_arsenic.csv", sep = ";")
arsenic 
x = arsenic$pH
y = arsenic$arsenic

#a)
cov(x, y)

#b)
cor(x, y) #strong realationship between the two values

#c)
plot(x, y, pch = 20)

#d)
line = lm(y~x)
line
#y_hat = 190.27 -18.03x -> y_hat is estimator not true value
abline(line)

#e)
#it wil decrease by 18.03

#f)
round(predict(line, data.frame(x = 7.5)))

#g)
round(predict(line, data.frame(x = 9)))

#i)
summary(line)
#model describes 90% of data

#j)
#H0: b == 0, H1: b !=0
#b -> slope of the function

test = anova(line)
pval = test$`Pr(>F)`[1]
alpha = 0.01
if(alpha > pval){
  print("reject H0")
}else{
  print("No reason to reject H0")
}

#TASK 3:
data = read.csv("Reg_3_bricks.csv", sep = ";")
x = data$Air
y = data$Dry

#H0: b1 = 0, HA: b!=0

#a
cov(x, y)

#b)
cor(x, y) #strong correlation of data

#c)
plot(x, y, pch = 20)

#d)
line = lm(y~x)
abline(line)
#y_hat = -0.92x + 126.25

#e)
#decreases by 0.92

#f)
round(predict(line, data.frame(x = 11)))

#g)
round(predict(line, data.frame(x = 23)))

#h)
summary(line)
#R-squared: 0.752
#the model describes 75% of data

#i)
alpha = 0.05
res = anova(line)
pval = res$`Pr(>F)`[1]
if (alpha > pval){
  print("reject H0")
}else{
  print("No reason to reject H0")
}

#TASK 4:
data = read.csv("Reg_4_time_temp.csv", sep = ";")
xx = na.omit(data$operation.time)
yy = na.omit(data$temperature)

#a)
cov(xx, yy)

cor(xx, yy) #weak correlation

#b), c), d)
plot(xx, yy)

rm(x)

model1 = lm(yy~xx)
summary(model1)
coefs1 = model1$coefficients
curve(coefs1[1] + coefs1[2]*x, add = T)


model2 = lm(yy~xx+I(xx^2))
summary(model2)
coefs2 = model2$coefficients
curve(coefs2[1] + coefs2[2]*x + coefs2[3]*x^2, add = T)

model3 = lm(yy~xx+I(xx^2)+I(xx^3))
summary(model3)
coefs3 = model3$coefficients
curve(coefs3[1] + coefs3[2]*x + coefs3[3]*x^2 + coefs3[4]*x^3, add = T)

#e)
alpha = 0.05
res = anova(model3)
pval = res$`Pr(>F)`[1]
if (alpha > pval){
  print("reject H0")
}else{
  print("No reason to reject H0")
}

#f)
round(predict(model3, data.frame(xx = 15.8)))

#g)
summary(model1) #5.29%
summary(model2) #5.80%
summary(model3) #76.6%
