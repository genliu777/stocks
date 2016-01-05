#!/usr/bin/bash

python_dir=../analysis/python/
R_dir=../analysis/R

sh_data_dir=e:/gww/MIT/stock/data/price/sh/xueqiu
sz_data_dir=e:/gww/MIT/stock/data/price/sz/xueqiu

day="2015-08-01"

$python_dir/dir_analysis.py $sh_data_dir $R_dir/R-pant.r $day
