from .inspection import categorize, add_notnull_variable

def preprocess(df):

    null_cols = ['Resolution', 'Time to Resolution', 'Customer Satisfaction Rating', 'First Response Time']

    # categorize gender variable into three categories: 'Male', 'Female' and 'Other'
    df = categorize(df, 'Customer Gender')

    # Add Boolean variables to evaluate NULL VALUES
    for col in null_cols:
        df = add_notnull_variable(df, col)

    return df