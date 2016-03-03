#!/usr/bin/env Rscript

library(RSQLite)

conn <- dbConnect(SQLite(), "../../sqlite_db/extra_stocks.db")
query<-dbSendQuery(conn, "select * from '300231_extra'")
quote<-fetch(query, n=-1)
quote

d1<-with(quote,  {data.frame(
	pr=price,
	r1=rratio1,
	r5=rratio5,
	r10=rratio10,
	r20=rratio20,
	r30=rratio30,
	r60=rratio60,
	v1=volume_ratio,
	vr5=volume_ratio_5,
	vr10=volume_ratio_10,
	vr20=volume_ratio_20,
	vr30=volume_ratio_30,
	vr60=volume_ratio_60,
	amp=amplitudes)
	})

factanal(x = d1, factors = 5, ratation = "promax")->ft
