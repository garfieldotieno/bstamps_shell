import redis
import api_master.config as config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a SQLAlchemy engine for the SQLite database
engine = create_engine('sqlite:///new_models.sqlite')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session instance
session = Session()

if config.redis_config['mode'] == 'DEVELOPMENT':
    bot_sites_db = redis.Redis(host="localhost", port=6379, db=1)

    mk40_bot_db = redis.Redis(host='localhost', port=6379, db=2)

    base_bot_db = redis.Redis(host='localhost', port=6379, db=3)

    blu_bot_db = redis.Redis(host='localhost', port=6379, db=4)

    hermes_bot_db = redis.Redis(host='localhost', port=6379, db=5)

    loca_db = redis.Redis(host="localhost", port=6379, db=6)

    swatsika_db = redis.Redis(host='localhost', port=6379, db=7)

else:
    bot_sites_db = redis.Redis(host="bstamps_shell-bredis-1", port=6379, db=1)

    mk40_bot_db = redis.Redis(host='bstamps_shell-bredis-1', port=6379, db=2)

    base_bot_db = redis.Redis(host='bstamps_shell-bredis-1', port=6379, db=3)

    blu_bot_db = redis.Redis(host='bstamps_shell-bredis-1', port=6379, db=4)

    hermes_bot_db = redis.Redis(host='bstamps_shell-bredis-1', port=6379, db=5)

    loca_db = redis.Redis(host="bstamps_shell-bredis-1", port=6379, db=6)

    swatsika_db = redis.Redis(host='bstamps_shell-bredis-1', port=6379, db=7)










