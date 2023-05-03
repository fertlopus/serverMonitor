### Small Scripy for monitoring server side changes in the specific directory
The repository contains script that is able to monitor the changes on the server side (e.g. file addition, file removing, file change,
file modification and etc.). The results of server changes will be written to the logs file or you can provide your own file and directory
to output.

To run the script you need the following dependencies:
- Python 3.4+
- <a href="https://pypi.org/project/pyinotify/"> pyinotify </a>
- Linux/MacOS operating system

To install the pyinotify run the following command in the terminal using pip manager:

`
$ pip3 install -m pyinotify
`

This will install the module to your environment.

To begin monitor server changes run the command:


~~~
$python3 notifier.py --monitor_dir './trash/' --logs_dir './logs.log'  --usr "UserName" --pwd "Password" --env "Environment"
~~~

The example of the logs file:

~~~
2021-07-01T10:59:39Z	IN_MODIFY	test.csv	/home/user/python_projects/messaging/trash/test.csv
2021-07-01T10:59:48Z	IN_CREATE	queue.txt	/home/user/python_projects/messaging/trash/queue.txt
2021-07-01T10:59:48Z	IN_MODIFY	queue.txt	/home/user/python_projects/messaging/trash/queue.txt
2021-07-01T11:00:04Z	IN_CREATE|IN_ISDIR	pathes	/home/user/python_projects/messaging/trash/pathes
2021-07-01T11:00:51Z	IN_DELETE|IN_ISDIR	tests_monitor	/home/user/python_projects/messaging/trash/tests_monitor
2021-07-01T11:00:51Z	IN_DELETE_SELF		/home/user/python_projects/messaging/trash/tests_monitor
2021-07-01T11:00:51Z	IN_IGNORED		/home/user/python_projects/messaging/trash/tests_monitor
2021-07-01T11:00:55Z	IN_DELETE	test.csv	/home/user/python_projects/messaging/trash/test.csv
2021-07-01T11:00:59Z	IN_DELETE	queue.txt	/home/user/python_projects/messaging/trash/queue.txt
2021-07-01T11:01:02Z	IN_DELETE|IN_ISDIR	pathes	/home/user/python_projects/messaging/trash/pathes
2021-07-01T11:01:02Z	IN_DELETE_SELF		/home/user/python_projects/messaging/trash/pathes
2021-07-01T11:01:02Z	IN_IGNORED		/home/user/python_projects/messaging/trash/pathes
2021-07-01T11:11:01Z	IN_MODIFY	test.csv	/home/user/python_projects/messaging/trash/test.csv

~~~~


