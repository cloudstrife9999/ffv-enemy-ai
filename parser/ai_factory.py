from .enemy_ai import EnemyAI
from .tokeniser import EnemyAITokeniser


class EnemyAIFactory():
    @staticmethod
    def create_ai(enemy_id: str, enemy_name: str, hex_ai: str) -> EnemyAI:
        tokens: list[list[int]] = EnemyAITokeniser.tokenise(enemy_id=enemy_id, hex_ai=hex_ai)

        return EnemyAI(enemy_id=enemy_id, enemy_name=enemy_name, raw=hex_ai, tokens=tokens)
