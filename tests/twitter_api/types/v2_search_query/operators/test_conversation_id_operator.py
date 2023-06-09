from twitter_api.types.v2_search_query.operators.conversation_id_operator import (
    ConversationIdOperator,
)
from twitter_api.types.v2_search_query.operators.operator import CompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestConversationIdOperator:
    def test_conversation_id_operator(self):
        assert (
            str(ConversationIdOperator("1334987486343299072"))
            == "conversation_id:1334987486343299072"
        )

    def test_query_complete(self):
        assert isinstance(
            build(lambda q: q.conversation_id("1334987486343299072")),
            CompleteOperator,
        )

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.conversation_id("1334987486343299072")))
            == "conversation_id:1334987486343299072"
        )
