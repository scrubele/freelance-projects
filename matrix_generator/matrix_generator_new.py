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
TRESHOLD_PREFIX = '_treshold'
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



def get_recipes_names(recipes_dataframe):
    """
    Function that forms recipes names row
    Input:
        # recipes_dataframe
    Output:
        # recipes names : List
    """
    recipes = list(recipes_dataframe[RECIPES_COLUMN_NAME].values)
    return recipes

def get_recipe_treshold_names(recipes_dataframe):
    recipe_names = list(recipes_dataframe.columns)[1:]
    return recipe_names

def get_matrix_treshold_names(matrix_dataframe):
    matrix_tresholds = list(matrix_dataframe.columns)[1:]
    return matrix_tresholds

def change_treshold_names(recipes_dataframe, matrix_dataframe):
    recipe_names = get_recipe_treshold_names(recipes_dataframe)
    matrix_tresholds = list(matrix_dataframe.columns)
    recipe_names = [recipe+TRESHOLD_PREFIX for recipe in recipe_names]
    matrix_tresholds = [matrix_tresholds[0]]+recipe_names
    matrix_dataframe.columns = matrix_tresholds

def are_row_equal(matrix_index, recipe_row, common_treshold_names):
    """
    Function that check if wallet's values are equal to recipe row values.
    Input:
        # matrix_row - wallet's row from the matrix data frame
        # recipe_row - recipe's row from the recipe data frame
    Output:
        # value is wallet's row equal to recipe's row : Boolean (True or False)
    """
    for treshold in common_treshold_names: 
        recipe_value = recipe_row[treshold].values[0]
        cell_value = matrix_dataframe.iloc[matrix_index][treshold+TRESHOLD_PREFIX]
        if recipe_value and not cell_value:
            return False
    return True

def are_wallets_equal_to_recipe(matrix_dataframe, recipe_row, common_treshold_names):
    """
    Function that iterate wallets and check if wallets'row values are equal to recipe row values.
    Input:
        # matrix_dataframe
        # recipe_row - recipe's row from the recipe data frame
    Output:
        # values which wallet's row is equal to recipe's row (which wallet like recipe) : Boolean list (True or False)
    """
    are_wallets_equal_to_recipe_list = []
    for matrix_index, matrix_row in matrix_dataframe.iterrows():
        # return wallet's treshold columns
        matrix_row = matrix_row[1]
        are_row_values_equal = are_row_equal(matrix_index, recipe_row, common_treshold_names)  # check equality
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

def form_recipe_column(recipe, recipes_dataframe, matrix_dataframe, common_treshold_names):
    """
    Function that form recipe column for the new matrix dataframe
    Input:
        # recipe
        # recipes_dataframe
        # matrix_dataframe
    Output:
        # ready recipe's column : Boolean List
    """
    recipe_row = recipes_dataframe.loc[recipes_dataframe[RECIPES_COLUMN_NAME]
                                      == recipe]
    recipe_column = are_wallets_equal_to_recipe(
        matrix_dataframe, recipe_row, common_treshold_names)  # check equality
    # form recipe row in the report list
    form_recipe_report_row(recipe, recipe_column)
    return recipe_column


def form_new_matrix(recipes_dataframe, matrix_dataframe):
    """
    Function that form recipe column for the new matrix dataframe
    Input:
        # recipes_dataframe
        # matrix_dataframe
    Output:
        # ready new matrix dataframe
    """
    new_matrix_dataframe = matrix_dataframe.copy()  # make a copy of the previous matrix
    recipes = get_recipes_names(recipes_dataframe)  # get recipes' names list
    common_treshold_names = recipes_dataframe.columns[1:]
    for recipe in recipes:
        recipe_column = form_recipe_column(
            recipe, recipes_dataframe, matrix_dataframe, common_treshold_names)  # form whole recipe's column
        # assign new recipe's column
        new_matrix_dataframe[recipe] = recipe_column
    return new_matrix_dataframe


def get_true_value_wallets(recipe, matrix_dataframe):
    """
    Function that form recipe's report row based on which wallets like recipe (have True value in the recipe's column)
    Input:
        # recipe
        # recipes_dataframe
    Output:
        # recipe's report row [recipe, wallets_that_like_recipe]
    """
    # form true-value wallets
    wallet_array = matrix_dataframe[WALLET_COLUMN_NAME].loc[matrix_dataframe[recipe] == True].values
    # convert wallet array to string
    wallets_string = str(list(wallet_array)).strip("[]")
    return [recipe, wallets_string]


def form_report(recipes_dataframe, matrix_dataframe):
    """
    Function that form recipe report
    Input:
        # recipes_dataframe
        # matrix_dataframe 
    Output:
        # ready new report list
    """
    report_list = []
    recipes = get_recipes_names(recipes_dataframe)
    for recipe in recipes:
        recipe_report_row = get_true_value_wallets(recipe, matrix_dataframe)
        report_list.append(recipe_report_row)
    result_dataframe = pd.DataFrame(report_list)
    return result_dataframe


if __name__ == '__main__':
    # Read pickle section
    recipes_dataframe = read_pickle(RECIPES_FILE_NAME)
    matrix_dataframe = read_pickle(MATRIX_FILE_NAME)
    # Change treshold names section
    change_treshold_names(recipes_dataframe, matrix_dataframe)
    # Write input files section
    # write_dataframe_to_csv(recipes_dataframe, RECIPES_FILE_NAME)
    # write_dataframe_to_csv(matrix_dataframe, MATRIX_FILE_NAME)
    # Form data section
    new_matrix_dataframe = form_new_matrix(recipes_dataframe, matrix_dataframe)
    report_list_dataframe = form_report(recipes_dataframe, new_matrix_dataframe)
    summary_report_dataframe = pd.DataFrame(summary_report)
    # # Print results section
    # print(new_matrix_dataframe)
    # print(report_list_dataframe)
    # print(summary_report_dataframe)
    # Save results section
    # write_dataframe_to_csv(new_matrix_dataframe, 'new_'+MATRIX_FILE_NAME)
    # write_dataframe_to_csv(report_list_dataframe, REPORT_FILE_NAME)
    # write_dataframe_to_csv(summary_report_dataframe, SUMMARY_REPORT_FILE_NAME)
