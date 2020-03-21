from flaskai.algorithms.linear_reg_alg import LinearRegressionAlg


class LinearRegService:

    linear = LinearRegressionAlg()

    def lin_get_multiple_var(self, investments, med_age, wins, equals, defeats, goals):
        return self.linear.lin_get_multiple_var(investments, med_age, wins, equals, defeats, goals)

    def draw_linear_regression(self, variable):
        return self.draw_linear_regression(variable)
