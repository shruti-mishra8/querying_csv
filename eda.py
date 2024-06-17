class QueryEda:
    def __init__(self, agent):
        self.agent = agent

    def qna(self, user_question):
        result = self.agent.invoke(user_question)

        # Extract only the output value
        if isinstance(result, dict) and "output" in result:
            return result["output"]

        return result

    def summary(self, user_eda_column):
        summary_statistics = self.agent.invoke(
            f"What are the mean, median, mode, standard deviation, variance, range, quartiles, skewness, and kurtosis {user_eda_column}"
        )
        outliers = self.agent.invoke(
            f"Assess the presence of outliers of {user_eda_column}"
        )
        missing_values = self.agent.invoke(
            f"Determine the extent of missing values of {user_eda_column}"
        )

        # Extract the relevant part of the response, assuming it's stored in a key called 'output'
        summary_text = summary_statistics.get("output", "")
        outliers_text = outliers.get("output", "")
        missing_values_text = missing_values.get("output", "")

        # Combine the extracted text
        combined_output = (
            summary_text + "\n\n" + outliers_text + "\n\n" + missing_values_text
        )

        return combined_output
