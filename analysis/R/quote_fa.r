#!/usr/bin/env Rscript

library(RSQLite)

conn <- dbConnect(SQLite(), "e:/gww/MIT/stock/sqlite_db/extra_stocks.db")
query<-dbSendQuery(conn, "select * from '603077_extra'")
quote<-fetch(query, n=-1)
quote

d1<-with(quote,  {
	pr<-price
	r1<-rratio1
	r5<-rratio5
	r10<-rratio10
	r20<-ratio20
	r30<-rratio30
	r60<-rratio60
	v1<-volume_ratio
	})


