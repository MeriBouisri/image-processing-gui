import logging

logging.getLogger().setLevel(logging.DEBUG)
handler = logging.StreamHandler()

handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s - line %(lineno)d, in %(funcName)s',
                           datefmt='%H:%M:%S')

handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)