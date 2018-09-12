#!/usr/bin/python3
from pyramid_sqlalchemy import Session as DB
import transaction
from tp_contest.models import School


with transaction.manager as tx:
    with open('~/Desktop/國小代碼.csv') as f:
        for each_line in f:
            sid, sname = each_line.strip().split(',')
            s = School()
            s.name = 
