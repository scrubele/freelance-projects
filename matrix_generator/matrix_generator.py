import pickle
import csv
import pandas as pd

report_results = []
RECIPES_COLUMN_NAME = 'Recipe'
MATRIX_FILE_NAME = 'matrix'
RECIPES_FILE_NAME = 'recipe'


def read_pickle(name):
    unpickled_df = pd.read_pickle(name+".pkl")
    # write_dataframe_to_csv(unpickled_df, name)
    return unpickled_df


def write_pickle(dataframe, name):
    dataframe.to_pickle(name+".pkl")
    write_dataframe_to_csv(dataframe, name)


def write_dataframe_to_csv(dataframe, name):
    dataframe.to_csv(name+".csv", sep='\t', encoding='utf-8')


def write_report_to_csv():
    with open('report.csv', mode='w') as report_file:
        report_writer = csv.writer(
            report_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        report_writer.writerow(
            [RECIPES_COLUMN_NAME, 'True_values_count', 'False_values_count'])
        for result in report_results:
            report_writer.writerow(result)


def are_rows_equal_to_recipe(matrix_dataframe, recipe_row):
    are_rows_equal_to_recipe_list = []
    for matrix_row in matrix_dataframe.iterrows():
        matrix_row = matrix_row[1].values[1:]
        are_row_values_equal = list(recipe_row == matrix_row)
        are_row_equal = False if are_row_values_equal.count(
            False) > 0 else True
        are_rows_equal_to_recipe_list.append(are_row_equal)
    return are_rows_equal_to_recipe_list


def str_recipe(recipe, recipe_column):
    result = [recipe, recipe_column.count(True), recipe_column.count(False)]
    report_results.append(result)
    print(result)


def form_recipe_column(recipe, recipe_dataframe, matrix_dataframe):
    recipe_row = recipe_dataframe.loc[recipe_dataframe[RECIPES_COLUMN_NAME]
                                      == recipe].values[0][1:]
    recipe_column = are_rows_equal_to_recipe(matrix_dataframe, recipe_row)
    str_recipe(recipe, recipe_column)
    return recipe_column


def iterate_recipes(recipe_dataframe, matrix_dataframe):
    new_matrix_dataframe = matrix_dataframe.copy()
    recipes = list(recipe_dataframe[RECIPES_COLUMN_NAME].values)
    for recipe in recipes:
        recipe_column = form_recipe_column(
            recipe, recipe_dataframe, matrix_dataframe)
        new_matrix_dataframe[recipe] = recipe_column
    return new_matrix_dataframe


if __name__ == '__main__':
    recipe_dataframe = read_pickle(RECIPES_FILE_NAME)
    matrix_dataframe = read_pickle(MATRIX_FILE_NAME)
    new_matrix_dataframe = iterate_recipes(recipe_dataframe, matrix_dataframe)
    write_report_to_csv()
    write_pickle(new_matrix_dataframe, 'new_'+MATRIX_FILE_NAME)
