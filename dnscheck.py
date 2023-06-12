#!/usr/bin/env python
# coding: UTF-8
#
import yaml
import time
import dns.resolver
from tabulate import tabulate

def read_config():
    with open('config.yml', 'r') as data:
        config = yaml.safe_load(data)
        return config

def query_run(server, port, name, querytype):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [server]
    resolver.port = port
    try:
      answer = resolver.resolve(name, querytype)
      answer = answer.rrset
      return answer
    except:
      pass

def main():
    config_data = read_config()

    headers = ["No", "Nameserver", "Port", "Query", "Match", "Query time[ms]", "Status"]
    table = []

    for index, params in enumerate(config_data['config'], 1):
        no = index
        name = params['name']
        server = params['server']
        port = params['port']
        qtype = 'A'
        match_string = params['match']

        record_start = time.perf_counter()
        query_result = query_run(
            server,
            port,
            name,
            qtype
        )
        record_end = time.perf_counter()

        execution_time = (record_end - record_start) * 1000
        execution_time = round(execution_time, 3)

        bucket = []
        if query_result:
            for x in query_result:
                y = x.to_text()
                bucket.append(y)

        if match_string in bucket:
            status = "PASS"
        else:
            status = "FAIL"

        table.append([no, server, port, name, match_string, execution_time, status])

    print(tabulate(table, headers, tablefmt="github"))

if __name__ == '__main__':
    main()