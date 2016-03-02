#! /usr/bin/Rscript

library(RSQLite)

conn <- dbConnect(SQLite(), "e:/gww/MIT/stock/sqlite_db/extra_stocks.db")
query<-dbSendQuery(conn, "select * from '603077_extra'")
quote<-fetch(query, n=-1)
quote


