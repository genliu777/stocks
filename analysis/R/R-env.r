#!/usr/bin/Rscript

f <- function(x)
{
 d<-eval.parent(c)

  print(x)
  print(d)
  
  e<-sys.frame(sys.parent())
  print(e)
  
  ll<-eval(objects(), envir=e)
  print(ll)
  
  l<-eval.parent(objects())
  print(l)
}

a <- 10
c<-11
a

f(a)





