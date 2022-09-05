# Columbia Fintech Bootcamp: Module #2 Challenge

Features:
- Python program that automates the tasks of valuing microlending loans - including automating loan and financial calculations, analyzing the loan data, and conditionally filter lists of loans.
- Additionally, the python program will prompt to the user to save the qualifiying loans as a new csv file.

---

## Technologies

This project leverages python 3.9 with the following packages:
* [fire](https://github.com/google/python-fire) - For the command line interface, help page, and entry-point.
* [questionary](https://github.com/tmbo/questionary) - For interactive user prompts and dialogs

*Assumption made for module challenge: the* **sys** *and Path module will not be required to be explicitely called out in Technologies section*

---

## Installation Guide

Before running the application first install the following dependencies.

```python
  pip install fire
  pip install questionary
```
*Assumption made for module challenge: the* **sys** *and Path module will not be required to be explicitely called out in Installation guide section*

---

## Usage

To use the loan qualification selection application, simply clone the repository and run the **app.py** script:

```python
python python app.py
```

Upon launching the loan qualification selection application, you will be prompted with the following.

> "Enter a file path to a rate-sheet (.csv): "


> "What's your credit score? "

> "What's your current amount of monthly debt? "

> " What's your total monthly income? "

> "What's your desired loan amount? "

> "What's your home value? "



You will then be notified of the number of qualifiying loans.



And promtped if where and if you would like to save the results (to a csv file):



> "Would you like to save the qualifying loans to a .csv file [Yes|No]?"


*Assumption made for module challenge: Prompt the user separately for the path/directory (confirm the path), followed by a prompt for the csv filename*

> "Enter a file path (directory) to write the qualifying loans:"

> "Enter a filename to write the qualifying loans (.csv):"



---
---

## Contributors

Contributors:
- Stratis Gavnoudias

---

## License

GNU General Public License (GPL).
