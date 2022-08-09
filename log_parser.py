import re
import json
import os
import glob
import argparse

parser = argparse.ArgumentParser(description='Process access.log')
parser.add_argument('-f', dest='file', action='store', default="C:\dev\linux_python_proj\logs", help='Path to logfile')
args = parser.parse_args()

METHODS = {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0,
           "HEAD": 0, "CONNECT": 0, "OPTIONS": 0, "TRACE": 0, }
REQUESTS_SCORE = 0
REQUESTS_SCORE_TOP_3 = {}
time_request_list = []
request_top_3_time = {}

for i in glob.glob(os.path.join(args.file, '*.log')):
    with open(i, 'r') as file:  # открываем все файлы
        for j in file:
            REQUESTS_SCORE += 1
            method = re.search(r"(POST|GET|PUT|DELETE|HEAD|CONNECT|OPTIONS|TRACE)", j)
            METHODS[method.group()] += 1
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", j)
            if ip_match.group(0) not in REQUESTS_SCORE_TOP_3:
                REQUESTS_SCORE_TOP_3[ip_match.group(0)] = 0
            else:
                REQUESTS_SCORE_TOP_3[ip_match.group(0)] += 1

            time_request = re.search("(\d{4,5}\n)", j)
            if time_request != None:
                time_request_final = re.search("(\d{4,5})", str(time_request))
                request_top_3_time[j] = int(time_request_final[0])

top_3_time = {} # ip с самым долгим ответом
for i in range(3):
    max_t = max(request_top_3_time, key=request_top_3_time.get)
    top_3_time[max_t] = request_top_3_time.pop(max_t)

top_3 = {} # ip с самым большим колличеством запросов
for i in range(3):
    max1 = max(REQUESTS_SCORE_TOP_3, key=REQUESTS_SCORE_TOP_3.get)
    top_3[max1] = REQUESTS_SCORE_TOP_3.pop(max1)

result = {"all_requests": 0, "all_methods": METHODS, "top_3_ip": top_3, "top_3_long_requests": top_3_time}
result["all_requests"] += REQUESTS_SCORE

with open('result.json', 'w') as result_file:
    json.dump(result, result_file)

print(f"all_requests                                     = {REQUESTS_SCORE}")
print(f"all_methods (типо запроса\колличество)           = {METHODS}")
print(f"top_3_ip (ip\колличество запросов )              = {top_3}")
print(f"top_3_long_requests(запрос\длитесьность)         = {top_3_time}")
