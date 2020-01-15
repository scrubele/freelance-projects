import pickle
import csv
import pandas as pd

# Files
MATRIX_FILE_NAME = 'matrix.pkl'
RECIPES_FILE_NAME = 'recipe.pkl'
REPORT_FILE_NAME = 'report.pkl'
SUMMARY_REPORT_FILE_NAME = 'summary_report.pkl'
# Columns
RECIPES_COLUMN_NAME = 'Recipe'
WALLET_COLUMN_NAME = 'consumer_wallet_id'
# Treshold sequence column numbers
FIRST_TRESHOLD_COLUMN_NUMBER = 1

summary_report = []  # Summary report matrix


def read_pickle(name):
    """
    Function that read pickle format file.
    You can delete it.
    """
    unpickled_dataframe = pd.read_pickle(name)
    return unpickled_dataframe


def write_pickle(dataframe, name):
    """
    Function that write pickle format file.
    You can delete it.
    """
    dataframe.to_pickle(name)
    write_dataframe_to_csv(dataframe, name)


def write_dataframe_to_csv(dataframe, name):
    dataframe.to_csv(name+".csv", sep='\t', encoding='utf-8')


def are_row_equal(matrix_row, recipe_row):
    """
    Function that check if wallet's values are equal to recipe row values.
    Input:
        # matrix_row - wallet's row from the matrix data frame
        # recipe_row - recipe's row from the recipe data frame
    Output:
        # value is wallet's row equal to recipe's row : Boolean (True or False)
    """
    true_count = list(recipe_row).count(True)  # Count True values number in the recipe's row.
    count = sum(recipe_row & matrix_row)
    # count is a sum of equal True and True values in the recipe's and wallet's rows.
    return true_count == count


def are_wallets_equal_to_recipe(matrix_dataframe, recipe_row):
    """
    Function that iterate wallets and check if wallets'row values are equal to recipe row values.
    Input:
        # matrix_dataframe
        # recipe_row - recipe's row from the recipe data frame
    Output:
        # values which wallet's row is equal to recipe's row (which wallet like recipe) : Boolean list (True or False)
    """
    are_wallets_equal_to_recipe_list = []
    for matrix_row in matrix_dataframe.iterrows():
        # return wallet's treshold columns
        matrix_row = matrix_row[1].values[FIRST_TRESHOLD_COLUMN_NUMBER:]
        are_row_values_equal = are_row_equal(
            matrix_row, recipe_row)  # check equality
        are_wallets_equal_to_recipe_list.append(are_row_values_equal)
    return are_wallets_equal_to_recipe_list


def form_recipe_report_row(recipe, recipe_column):
    """
    Function that form recipe's row for the report list data frame
    Input:
        # recipe
        # recipe_column - recipe's column from the recipe data frame
    Output:
        # a number of True and False values : List
    """
    result = [recipe, recipe_column.count(True), recipe_column.count(False)]
    summary_report.append(result)
    print(result)


def get_recipes_names(recipe_dataframe):
    """
    Function that forms recipes names row
    Input:
        # recipe_dataframe
    Output:
        # recipes names : List
    """
    recipes = list(recipe_dataframe[RECIPES_COLUMN_NAME].values)
    return recipes


def form_recipe_column(recipe, recipe_dataframe, matrix_dataframe):
    """
    Function that form recipe column for the new matrix dataframe
    Input:
        # recipe
        # recipe_dataframe
        # matrix_dataframe
    Output:
        # ready recipe's column : Boolean List
    """
    recipe_row = recipe_dataframe.loc[recipe_dataframe[RECIPES_COLUMN_NAME]
                                      == recipe].values[0][FIRST_TRESHOLD_COLUMN_NUMBER:]  # return recipe's treshold columns
    recipe_column = are_wallets_equal_to_recipe(
        matrix_dataframe, recipe_row)  # check equality
    # form recipe row in the report list
    form_recipe_report_row(recipe, recipe_column)
    return recipe_column


def form_new_matrix(recipe_dataframe, matrix_dataframe):
    """
    Function that form recipe column for the new matrix dataframe
    Input:
        # recipe_dataframe
        # matrix_dataframe
    Output:
        # ready new matrix dataframe
    """
    new_matrix_dataframe = matrix_dataframe.copy()  # make a copy of the previous matrix
    recipes = get_recipes_names(recipe_dataframe)  # get recipes' names list
    for recipe in recipes:
        recipe_column = form_recipe_column(
            recipe, recipe_dataframe, matrix_dataframe)  # form whole recipe's column
        # assign new recipe's column
        new_matrix_dataframe[recipe] = recipe_column
    return new_matrix_dataframe


def get_true_value_wallets(recipe, matrix_dataframe):
    """
    Function that form recipe's report row based on which wallets like recipe (have True value in the recipe's column)
    Input:
        # recipe
        # recipe_dataframe
    Output:
        # recipe's report row [recipe, wallets_that_like_recipe]
    """
    # form true-value wallets
    wallet_array = matrix_dataframe[WALLET_COLUMN_NAME].loc[matrix_dataframe[recipe] == True].values
    # convert wallet array to string
    wallets_string = str(list(wallet_array)).strip("[]")
    return [recipe, wallets_string]


def form_report(recipe_dataframe, matrix_dataframe):
    """
    Function that form recipe report
    Input:
        # recipe_dataframe
        # matrix_dataframe 
    Output:
        # ready new report list
    """
    report_list = []
    recipes = get_recipes_names(recipe_dataframe)
    for recipe in recipes:
        recipe_report_row = get_true_value_wallets(recipe, matrix_dataframe)
        report_list.append(recipe_report_row)
    result_dataframe = pd.DataFrame(report_list)
    return result_dataframe


if __name__ == '__main__':
    # Read pickle section
    recipe_dataframe = read_pickle(RECIPES_FILE_NAME)
    matrix_dataframe = read_pickle(MATRIX_FILE_NAME)
    # Form data section
    new_matrix_dataframe = form_new_matrix(recipe_dataframe, matrix_dataframe)
    report_list_dataframe = form_report(recipe_dataframe, new_matrix_dataframe)
    summary_report_dataframe = pd.DataFrame(summary_report)
    # Print results section
    print(new_matrix_dataframe)
    print(report_list_dataframe)
    print(summary_report_dataframe)
    # Save results section
    # write_dataframe_to_csv(new_matrix_dataframe, 'new_'+MATRIX_FILE_NAME)
    # write_dataframe_to_csv(report_list_dataframe, REPORT_FILE_NAME)
    # write_dataframe_to_csv(summary_report_dataframe, SUMMARY_REPORT_FILE_NAME)