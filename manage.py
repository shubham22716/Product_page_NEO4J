#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
from neo4j import GraphDatabase  
#uri= ("bolt://192.168.1.61:7687")
#driver = (GraphDatabase.driver(uri, auth=('devendra', '6df126ff'),database='movies'))

uri = []
uri.append("bolt://192.168.1.61:7687")
uri.append("bolt://192.168.1.62:7687")
uri.append("bolt://192.168.1.63:7687")
uri.append("bolt://192.168.1.64:7687")
uri.append("bolt://192.168.1.65:7687")
uri.append("bolt://192.168.1.66:7687")
uri.append("bolt://192.168.1.67:7687")

driver = [] 
count=0
for i in range(len(uri)):
    try:
        driver.append(GraphDatabase.driver(uri[i], auth=('devendra', '6df126ff'),database='customers'))
        count = count+1
    except:
        print(uri[i]+" is not working")
print(count)
driver = driver[0]



import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
