#!/usr/bin/env python
import common
from datetime import datetime

date_format = "%Y,%m,%d"
start = common.ask("Enter the start date:", answer=common.dateObject, dateformat='%Y,%m,%d')
end = common.ask("Enter the end date:", answer=common.dateObject, dateformat='%Y,%m,%d')
start_date = datetime.strptime(start, date_format)
end_date = datetime.strptime(end, date_format)
delta = end_date - start_date
print(delta.days)
