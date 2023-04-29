"""
Log4Python configuration
"""
config = {
    # 'monitorInterval': 10,  # auto reload time interval [secs]
    'loggers': {
        'NetScan': {
            'level': "DEBUG",
            'additivity': False,
            'AppenderRef': ['console', 'output']
        },
        'root': {
            'level': "WARN",
            'AppenderRef': ['output']
        }
    },
    'appenders': {
        'output': {
            'type': "file",
            'FileName': "./logs/default.log",  # log file name
            'backup_count': 5,  # files count use backup log
            'file_size_limit': 1024 * 1024 * 20,  # single log file size, default :20MB
            'PatternLayout': "[%(asctime)s] %(levelname)s (%(filename)s-:%(lineno)d) - %(message)s"
        },
        'console': {
            'type': "console",
            'target': "console",
            'PatternLayout': "[%(asctime)s] %(levelname)s (%(filename)s-:%(lineno)d) - %(message)s"
        }
    }
}
