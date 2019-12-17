# Note: Make sure you set the correct working directory using setwd("desired/path"). 
# Before that check the current the current directory by using getwd()

# Change the name for the required .csv file that you are testing with.
# Change to TRUE if you use headings for the csv columns.
df <- read.csv2("moveData2.csv", FALSE, ",")

# V1, V2, V3, V4, V5, V6 are the columns for the date so use it accordingly.
df1 <- ISOdate(df$V1,df$V2,df$V3,df$V4, df$V5, df$V6)

plot(df1, df$V8, xlab = "Time", ylab = "Angle", main = "Angle of flexion over a period of time", type = "l")


# To run the code execute 'source("angleofflexion.r", echo = FALSE)' in the Console.
# Set echo = TRUE if you want the commands to display in the console after parsing.