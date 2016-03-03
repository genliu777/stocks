#!/usr/bin/env python

import sqlite3
import logging

def amplitudes(quote):
	amp = []
	l = len(quote)
	Open, High, Low = (1,2,3)	
	for i in range(0,l):
		my_amp = (quote[i][High] - quote[i][Low]) / quote[i][Open]
		amp.append(my_amp)
	return amp

def volume_ratio_average_calculate(vr, interval):
	#quote is increae by day
	l = len(vr)
	get_vr = lambda x,y:x[y][1]
	vra = []
	summary = 0
	for i in range(0,l):
		summary += get_vr(vr, i) 
		if i < interval:
			my_vra = summary / (i+1)
		else:
			pre_my_vra = vra[i-1]
			my_vra = pre_my_vra + (get_vr(vr, i) - get_vr(vr, i-interval)) / interval
		vra.append(my_vra)
	return vra

def volume_ratio_average(vr):
	vra5 = volume_ratio_average_calculate(vr, 5)	
	vra10 = volume_ratio_average_calculate(quote, 10)
	vra20 = volume_ratio_average_calculate(quote, 20)	
	vra30 = volume_ratio_average_calculate(quote, 30)	
	vra60 = volume_ratio_average_calculate(quote, 60)	

	return vra5,vra10,vra20,vra30,vra60

def moving_average_calculate(quote, interval):
	#quote is increae by day
	l = len(quote)
	price = lambda x,y:x[y][1]
	ma = []	
	summay = 0
	for i in range(0,l):
		summay += 	price(quote, i)
		if i - interval < 0:
			my_ma = summay / (i+1)
		else:
			pre_price = price(quote, i-interval)
			pre_ma = ma[i-1]
			my_ma = pre_ma + (price(quote, i) - pre_price)/interval

		ma.append(my_ma)
	return ma
	
def moving_average(quote):
	ma5 = moving_average_calculate(quote, 5)
	ma10 = moving_average_calculate(quote, 10)
	ma20 = moving_average_calculate(quote, 20)
	ma30 = moving_average_calculate(quote, 30)
	ma60 = moving_average_calculate(quote, 60)

	return ma5,ma10,ma20,ma30,ma60

def rise_ratio_calculate(quote, interval):
	l = len(quote)
	dd = []	
	for i in range(0,l):
		close_price = quote[i][1]
		if (i-interval) < 0	:
			dd.append(0)
		else:
			pre_close_price = quote[i-interval][1]
			dd.append(float(close_price)/float(pre_close_price) - 1)
	
	return dd

def rise_ratio(quote):
	d1 = rise_ratio_calculate(quote, 1)
	d5 = rise_ratio_calculate(quote, 5)
	d10 = rise_ratio_calculate(quote, 10)
	d20 = rise_ratio_calculate(quote, 20)
	d30 = rise_ratio_calculate(quote, 30)
	d60 = rise_ratio_calculate(quote, 60)
	return d1,d5,d10,d20,d30,d60

def get_stock_quote(stock_code, connect):
	try:
		sql = "select * from '{0}'".format(stock_code)  
		cursor = connect.cursor()
		cursor.execute(sql)	
		return cursor.fetchall()
	except:
		return None

def get_stock_struct(stock_code):
	try:
		conn = sqlite3.connect("ss.db")
		cursor = conn.cursor()
		stock_struct_sql = "select * from '{0}_stock_struct'".format(stock_code)
		cursor.execute(stock_struct_sql)
		stock_struct = cursor.fetchall()

		Day,Amount,Flow_Restrict, Other, Flow, Flow_A = {0,1,2,3,4,5}	

		conn.commit()
		conn.close()
		return stock_struct
	except:
		return None


def get_amount(stock_struct, day=None):
	Day,Amount,Flow_Restrict, Other, Flow, Flow_A = {0,1,2,3,4,5}	
	if day == None:
		ss = stock_struct[0]
		return ss[Day], ss[Amount],ss[Flow_A]

	#stock_struct is decrease by day
	for ss in stock_struct:
		if cmp(ss[Day], day) < 1:
			return ss[Day], ss[Amount],ss[Flow_A]

	return  None
				
	
def dividend_price(quote, stock_struct):
	Close_price = 4
	get_price = lambda x,y:x[y][Close_price]
	
	get_day = lambda x,y:x[y][0]

	Day,Amount,Flow_Restrict, Other, Flow, Flow_A = {0,1,2,3,4,5}	
	today_amount = get_amount(stock_struct)

	#before right
	dp = []

	for i in range(0,len(quote)):
		amount = get_amount(stock_struct, quote[i][0])	
		if amount != None:
			dp.append((quote[i][0], quote[i][Close_price] *  \
				(float(today_amount[1]) / float(amount[1])))) 
	
	return dp

def volumn_ratio_info(quote, stock_struct):
	vr = []	
	Day,Amount,Flow_Restrict, Other, Flow, Flow_A = {0,1,2,3,4,5}	
	today_amount = get_amount(stock_struct)
	
	for i in range(0,len(quote)):
		amount = get_amount(stock_struct, quote[i][0])	
		if amount != None:
			vri = float(quote[i][5]) / float(amount[2]) / 10000
			vr.append((quote[i][0], vri))
	return vr

def make_qutoe_extra_tabel(conn, stock_code, price, m_average, r_ratio, volume_ratio, volume_ratio_average, amp):
	cursor = conn.cursor()
	sql = "create table '{0}_extra' (day text, price float, \
					ma5 float, ma10 float, ma20 float, ma30 float, ma60 float, \
					rratio1 float, rratio5 float, rratio10 float, rratio20 float,  \
					rratio30 float, rratio60 float, volume_ratio, volume_ratio_5, \
					volume_ratio_10, volume_ratio_20, volume_ratio_30, volume_ratio_60, \
					amplitudes)".format(stock_code)
	cursor.execute(sql)

	l = len(volume_ratio)

	for i in range(0, l):
		sql = "insert into '{0}_extra' values ('{1}', {2}, \
						{3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, \
						{11}, {12}, {13}, {14}, {15}, {16}, {17}, \
						{18}, {19}, {20})".format(stock_code, volume_ratio[i][0], price[i][1], \
							m_average[0][i], m_average[1][i], m_average[2][i], \
							m_average[3][i], m_average[4][i], \
							r_ratio[0][i], r_ratio[1][i], r_ratio[2][i], r_ratio[3][i], \
							r_ratio[4][i],r_ratio[5][i], \
							volume_ratio[i][1], volume_ratio_average[0][i], \
							volume_ratio_average[1][i], volume_ratio_average[2][i], \
							volume_ratio_average[3][i], volume_ratio_average[4][i], amp[i])

		print sql
		cursor.execute(sql)


def stocks_list(connect, market):
	cursor = connect.cursor()
	if market == "sh":
		sql = "select code from 'stocks' where market = 1"	
	elif market == "sz":
		sql = "select code from 'stocks' where market = 2"	
	cursor.execute(sql)
	ret = cursor.fetchall()
	return ret

if __name__ == "__main__":
#	conn = sqlite3.connect("../data/stock_db/stocks.db")
	conn = sqlite3.connect("stocks.db")
	extra_conn = sqlite3.connect("extra_stocks.db")

	sz_stocks = stocks_list(conn, "sz")
	
	for stocks in sz_stocks:
		stock_code =  stocks[0]

		quote = get_stock_quote(stock_code, conn)
		if quote == None:
			continue

		stock_struct = get_stock_struct(stock_code)
		if stock_struct == None:
			continue

		dp = dividend_price(quote, stock_struct)	
		vr = volumn_ratio_info(quote, stock_struct)
	
		rr = rise_ratio(dp)
		ma = moving_average(dp)
		vra = volume_ratio_average(vr)
		amp = amplitudes(quote)

		make_qutoe_extra_tabel(extra_conn, stock_code, dp, ma, rr, vr, vra, amp)

	extra_conn.commit()
	extra_conn.close()
	conn.commit()
	conn.close()
