import os

token = None


def get_token():
	global token

	if not token:
		try:
			token = os.environ["NAMESILO_TOKEN"]

		except:
			raise

		finally:
			return token
