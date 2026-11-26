
from myapp.extensions import db
from myapp.models.answer import Answer
from myapp.services.strategies import LLMStrategy


class AgentService:

    def __init__(self, strategy: LLMStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: LLMStrategy):
        self.strategy = strategy

    def generate_answer(self, question: str) -> str:
        return self.strategy.generate_response(question)

    def tiene_tag_ia_help(self, question) -> bool:
        return any(
            tag.name.lower().strip() in ("#ia-help", "ia-help")
            for tag in question.tags
        )

    def process_question(self, question):
        if not self.tiene_tag_ia_help(question):
            return None

        response_text = self.generate_answer(question.text)

        answer = Answer(
            text=response_text,
            question_id=question.id,
            user_id=None,
            author_type="AGENT",
            is_accepted=False
        )

        db.session.add(answer)
        db.session.commit()

        return answer
