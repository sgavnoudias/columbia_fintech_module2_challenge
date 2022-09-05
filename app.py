# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys
import fire
import questionary
from pathlib import Path

# Import the functions from the utils library module to load and save csv files
from qualifier.utils.fileio import (
    load_csv,
    save_csv
)

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value


def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_csv(csvpath)


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    print()

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print()
    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered


def save_qualifying_loans(qualifying_loans):
   """Saves the qualifying loans to a CSV file.

   Args:
      qualifying_loans (list of lists): The qualifying bank loans.
   """

   is_got_valid_cli_response = False  # A boolean to confirm a valid response from the user (will be set to True once the response from user is valid)
   # Prompt the user for various loan responses to satisfy business requirements (If the user does not provide a valid entry, loop through the prompts again)
   while (not is_got_valid_cli_response):

      if (len(qualifying_loans) > 0):

         # Business requirement:
         #   Given that I have a list of qualifying loans, when I’m prompted to save the results, then I should be able to opt out of saving the file.
         should_save_qualifying_loans = questionary.confirm("Would you like to save the qualifying loans to a .csv file?").ask()

         # Chek if user would like to save to csv file (should_save_qualifying_loans = True)
         if (should_save_qualifying_loans == True):
            is_got_valid_cli_response = True

            # Business requirement:
            #   Given that I have a list of qualifying loans, when I choose to save the loans, the tool should prompt for a file path to save the file.
            csvpath_str = questionary.text("Enter a file path (directory) to write the qualifying loans:").ask()
            csvpath = Path(csvpath_str)
            # Check that a valid path/directory was provided.  If not, notify the user and set the valid user response boolean to False to loop back and try again
            if not csvpath.exists():
               print(f"Oops! Can't find this path: {csvpath}, please try again.")
               is_got_valid_cli_response = False
            else:
               is_got_valid_cli_response = True

               # Business requirement:
               #      Given that I’m using the loan qualifier CLI, when I run the qualifier, then the tool should prompt the user to save the results as a CSV file
               csvfile_str = questionary.text("Enter a filename to write the qualifying loans (.csv):").ask()

               # Aggregate the user provided path (directory) and filename together
               csvpathfile_str = csvpath_str + "/" + csvfile_str
               csvpath = Path(csvpathfile_str)
               print("Saving qualifying loans to csv file: ", csvpath, ".  Thank you.  Exiting!")

               # Business requirement:
               #     Given that I’m using the loan qualifier CLI, when I choose to save the loans, then the tool should save the results as a CSV file.
               save_csv(csvpath, qualifying_loans)

         else:
            print("OK, will not save qualifying loan results to csv file.  Exiting!")
            is_got_valid_cli_response = True

      else:
         # Business requirement:
         #   Given that no qualifying loans exist, when prompting a user to save a file, then the program should notify the user and exit.
         print("Sorry, you do not have any qualifying loans.  Exiting!")
         is_got_valid_cli_response = True

      print()

def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)


if __name__ == "__main__":
    fire.Fire(run)
