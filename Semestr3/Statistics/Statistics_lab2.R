setwd("C:/Users/Kuba/Desktop/Studia/Semestr 3/Statystyka/Laboratories")

#TASK 1:
A=na.omit(read.csv2("flights.csv", sep=";"))
#a)
class(A)
A
#b)
hist(A[,1]) #wrong histogram -> shouldn't be any gaps
hist(A[, 1], breaks=4)

names=colnames(A)
names
par(mfrow = c(2, 3))
for (i in 1:6){
  hist(A[,i], breaks=4, main=paste("YEAR 195", i-1, sep=""), col=i)
  head(A)
}
#c)
for (i in 1:6){
  print(paste("For year ", names[i]))
  print(paste("Mean is:", round(mean(A[, i]), 2), "- average of the set"))
  print(paste("Min:", min(A[, i]))) #0 quartile
  print(paste("Quartile 1:", quantile(A[, i])[2])) #25% element
  print(paste("Quartile 2 (median):", quantile(A[, i])[3], "- it means that this is the middle element - at least half is greater or equal and at least half is smaller or equal")) #third quantile is median; however quantile != quartile (always quarters)
  print(paste("Quartile 3:", quantile(A[, i])[4])) #75% element
  print(paste("Max:", max(A[, i]))) #fourth quartile
  print(paste("Standard deviation is:", round(sd(A[,i]), 2), "- this much elements deviates from the mean on average"))
  print(paste("Variability index is:", round(100*sd(A[,i])/mean(A[, i]), 2)))
  print(" ")
}

#d)
for (i in 1:6){
  boxplot(A[, i], main = names[i])
}

#TASK 2:
B=na.omit(read.csv2("notes.csv"))
B
par(mfrow=c(2,2))
names = colnames(B)
#a)
for (i in 1:4){
  print(names[i])
  print(na.omit(table(B[,i])))
}
#b)
x = 1:10
x
for (i in 1:4){
  discrete.histogram(B[, i], main = names[i], xlab = "Grade", xlim = c(2, 5))
}

#c)
for (i in 1:4){
  print(paste("For", names[i]))
  print(paste("Mean is:", round(mean(B[, i]), 2), "- it means that this is average"))
  print(paste("Min:", min(B[, i]))) #0 quartile
  print(paste("Quartile 1:", quantile(B[, i])[2])) #25% element
  print(paste("Quartile 2 (median):", quantile(B[, i])[3], "- it means that this is the middle element and at least half is greater or equal and at least half is smaller or equal")) #third quantile is median; however quantile != quartile (always quarters)
  print(paste("Quartile 3:", quantile(B[, i])[4])) #75% element
  print(paste("Max:", max(B[, i]))) #fourth quartile  print(paste("Standard deviation is:", round(sd(na.omit(B[,i])), 2), "- this much elements deviates from the mean on average"))
  print(paste("Variability index is:", round(100*sd(na.omit(B[,i]))/mean(na.omit(B[, i])), 2)))
  print(" ")
}

#d)
par(mfrow = c(1, 1))
boxplot(B[, 1], B[, 2], B[, 3], B[, 4], main = "Comparison between groups")
#Black line = median (second quartile)
#Lower bound of gray area = first quartile
#Upper bound of gray area = third quartile
#Upper and lower lines are equal to 1,5 of difference between 1 and 3 quartile
#White dots are outliers

#e)
par(mfrow = c(2, 2))
for (i in 1:4){
  print (names[i])
  print(table(B[, i]))
  pie(table(B[, i]), main = paste("Pie chart for", names[i]))
}

#TASK 3:
#a)
C=na.omit(read.csv("strawberries.csv", sep=";"))
C

year_2000=length(C[, 1])
year_2000
year_2010=length(na.omit(C[, 2]))
year_2010

#b)
our_table1 = table(cut(C[, 1], breaks=5))
our_table1
our_table2 = table(cut(C[, 2], breaks=5))
our_table2

#c)
#discrete.histogram(our_table1, freq=F)
#hist(our_table1, freq=F)

par(mfrow = c(1, 2)) #how big is display -> 1 row two columns
#freq = F -> we will have probabilities, freq = T -> we will have number of appearances
for (i in 1:2){
  hist(C[, i], freq = F, breaks = 5, main = paste("Year number 20", i-1, "0", sep=""), xlab="number of strawberries", col = i+5)
}

#d)
names = colnames(C)
for (i in 1:2){
  print(paste("For", names[i]))
  print(paste("Mean is:", round(mean(C[, i]), 2), "- it means that this is average"))
  print(paste("Min:", min(C[, i]))) #0% element == 0th element
  print(paste("Quartile 1:", quantile(C[, i])[2])) #25% element
  print(paste("Quartile 2 (median):", quantile(C[, i])[3], "- it means that this is the middle element and at least half is greater or equal and at least half is smaller or equal")) #50% (middle) element
  print(paste("Quartile 3:", quantile(C[, i])[4])) #75% element
  print(paste("Max:", max(C[, i]))) #100% element == 4th quartile
  print(paste("Variability index is:", round(100*sd(C[,i])/mean(C[, i]), 2)))
  print(" ")
}

#probability measures = mean, median, quantiles, min, max, stand_dev, variability index

#e)
par(mfrow = c(1, 1))
boxplot(na.omit(C[, 1]), na.omit(C[, 2]))
#black line - median, first  and third quartile (grey area) and lowest/highest element not being outlier (pozioma linia -> Q1 - IQR)

#f)
par(mfrow = c(1, 2))
for (i in 1:2){
  #print(na.omit(summary(C[, i]))) -> display of basic stats
  pie(table(cut(C[, i], breaks = 5)), main = names[i])
  print("Frequency interval table:")
  print(table(cut(na.omit(C[, i]), breaks = 5)))
}
