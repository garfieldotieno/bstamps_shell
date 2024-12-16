import redis 

DATABASES = {
  "default": "mysql",
  "mysql": {
    "host": "127.0.0.1",
    "driver": "mysql",
    "database": "masonite",
    "user": "root",
    "password": "",
    "port": 3306,
    "log_queries": False,
    "options": {
      #
    }
  },
  "postgres": {
    "host": "127.0.0.1",
    "driver": "postgres",
    "database": "masonite",
    "user": "root",
    "password": "",
    "port": 5432,
    "log_queries": False,
    "options": {
      #
    }
  },
  "sqlite": {
    "driver": "sqlite",
    "database": "hermes.sqlite3",
  }

}


# hermes_bot_db = redis.Redis(
#     host='bstamps_shell-bredis-1',  # Redis server host
#     port=6379,         # Redis server port
#     db=3,              # Database number (default is 0)
#     decode_responses=True  # Automatically decode responses to strings
# )

hermes_bot_db = redis.Redis(
    host='localhost',  # Redis server host
    port=6379,         # Redis server port
    db=3,              # Database number (default is 0)
    decode_responses=True  # Automatically decode responses to strings
)
