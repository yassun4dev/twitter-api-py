from twitter_api.types.v2_user.username import Username

from ._specific_keyword import SpecificKeyword
from .operator import Operator


class MentionOperator(SpecificKeyword, Operator[Operator]):
    def __init__(self, username: Username):
        super().__init__(username, "@")