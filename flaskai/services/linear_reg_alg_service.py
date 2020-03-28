from flaskai.algorithms.linear_reg_alg import LinearRegressionAlg


class LinearRegService:

    linear = LinearRegressionAlg()

    def lin_get_multiple_var(self, investments, med_age, wins, equals, defeats, goals):
        result = self.linear.lin_get_multiple_var(investments, med_age, wins, equals, defeats, goals)[0]
        print(result)
        dictionary_to_return = {"result": result}
        return dictionary_to_return

    def draw_linear_regression(self, variable):
        return self.linear.draw_linear_regression(variable)
