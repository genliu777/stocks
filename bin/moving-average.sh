#!/usr/bin/bash

python_dir=../analysis/python/
R_dir=../analysis/R

sh_data_dir=d:/MIT/stock/data/price/sh/xueqiu
sz_data_dir=d:/MIT/stock/data/price/sz/xueqiu

day="2015-12-21"

$python_dir/dir_analysis.py $sh_data_dir $R_dir/R-moving-average.r $day
