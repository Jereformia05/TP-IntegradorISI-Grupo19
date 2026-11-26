from myapp.extensions import db
from myapp.models.answer import Answer
from myapp.services.strategies import LLMStrategy, MockLLMStrategy


class AgentService:
    def __init__(self, strategy: LLMStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: LLMStrategy):
        self.strategy = strategy

    def generate_answer(self, question: str) -> str:
        return self.strategy.generate_response(question)

    def tiene_tag_ia_help(self, question) -> bool:
        tags = getattr(question, "tags", None) or []
        return any(
            getattr(tag, "name", "").lower().strip() in ("#ia-help", "ia-help")
            for tag in tags
        )

    def process_question(self, question):
        if not self.tiene_tag_ia_help(question):
            return None

        question_text = getattr(question, "content", None) or getattr(question, "text", "")
        response_text = self.generate_answer(question_text)

        answer = Answer(
            content=response_text,
            question_id=question.id,
            user_id=None,
            author_type="AGENT",
            is_accepted=False,
        )

        db.session.add(answer)
        db.session.commit()

        return answer


_default_agent_service = AgentService(strategy=MockLLMStrategy())


def process_question_for_agent(question):
    if question is None:
        return None
    try:
        return _default_agent_service.process_question(question)
    except Exception:
        return None