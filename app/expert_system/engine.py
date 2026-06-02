from experta import KnowledgeEngine, Fact, Rule, AND, L


class UserProfile(Fact):
    """User fitness profile fact."""
    pass


class PhysiqExpertEngine(KnowledgeEngine):

    @Rule(UserProfile(fitness_level=L("beginner")))
    def beginner_plan(self):
        self.declare(Fact(recommendation="3x/week full-body, low intensity"))

    @Rule(UserProfile(fitness_level=L("intermediate")))
    def intermediate_plan(self):
        self.declare(Fact(recommendation="4x/week push-pull split, moderate intensity"))

    @Rule(UserProfile(fitness_level=L("advanced")))
    def advanced_plan(self):
        self.declare(Fact(recommendation="5x/week PPL split, high intensity"))

    @Rule(AND(UserProfile(goal=L("weight_loss")), UserProfile(fitness_level=L("beginner"))))
    def weight_loss_beginner(self):
        self.declare(Fact(cardio="30min moderate cardio 3x/week"))

    def run(self, user_data: dict) -> dict:
        self.reset()
        self.declare(UserProfile(**user_data))
        super().run()

        results = {}
        for fact in self.facts.values():
            if isinstance(fact, Fact) and fact is not self.facts[0]:
                results.update(dict(fact))
        return results
