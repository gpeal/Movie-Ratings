class BaseAdapter(object):
    """Base Adapter

    Interface to implement movie database adapters.

    """
    def __init__(self, name):
        self.name = name

    def get_score(self, title):
        """Get Score

        Returns a list of dictionaries containing 'title' and 'score' of the top 5 movie hits.

        """
        raise NotImplementedError('Interface not defined')