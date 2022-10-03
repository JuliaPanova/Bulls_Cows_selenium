import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os


def parse_answer(s_ans):
    num = s_ans[:4]
    cows = int(s_ans[7])
    bulls = int(s_ans[20])
    return num, cows, bulls


def count_cows_bulls(secret_num, ans_num):
    cows, bulls = 0, 0
    for i in range(len(ans_num)):
        if ans_num[i] == secret_num[i]:
            bulls += 1
        elif ans_num[i] in secret_num:
            cows += 1
    return cows, bulls


def test_bulls_cows_until_win():
    list_answers = []
    chrome_driver = open_frame()
    for num in range(1000, 10000):
        s_num = str(num)
        if len(set(list(s_num))) == 4:
            answer = enter_number_and_click(chrome_driver, s_num)
            list_answers.append(answer)
            if answer.find("WIN") >= 0:
                break
    else:
        assert False, "No secret number found"

    secret_number = list_answers[-1][:4]
    for i in range(len(list_answers) - 1):
        ans = list_answers[i]
        entered_number, answer_cows, answer_bulls = parse_answer(ans)
        expected_cows, expected_bulls = count_cows_bulls(secret_number, entered_number)
        assert (expected_cows, expected_bulls) == (answer_cows, answer_bulls), f'Secret number: {secret_number}, entered number:{entered_number}, ' +\
            f'expected: {expected_cows} cow(s), {expected_bulls} bull(s), actual: {answer_cows} cow(s), {answer_bulls} bull(s)'

    chrome_driver.close()


def open_frame():
    os.environ['PATH'] += r';C:\Program Files (x86)\Google\Chrome\Application'
    chrome_driver = webdriver.Chrome()

    chrome_driver.get('https://codepen.io/BilelJ/pen/RZOqJX')
    chrome_driver.maximize_window()
    sleep(3)

    chrome_driver.switch_to.frame(chrome_driver.find_element(By.TAG_NAME, "iframe"))
    return chrome_driver


def enter_number_and_click(chrome_driver, number):
    input_text = chrome_driver.find_element(By.ID, "try")
    input_text.send_keys(number)
    button = chrome_driver.find_element(By.ID, "submit")
    button.click()
    console = chrome_driver.find_element(By.ID, "console")
    content = console.get_attribute('value')
    return content.split("\n")[0]


def test_bulls_cows_number_too_short():
    chrome_driver = open_frame()
    number = 123
    response = enter_number_and_click(chrome_driver, number)
    assert 'Invalid entry' in response, f'Expected: error message'
    chrome_driver.close()


def test_bulls_cows_duplicated_digits():
    chrome_driver = open_frame()
    number = 1233
    response = enter_number_and_click(chrome_driver, number)
    assert 'Invalid entry' in response, f'Expected: error message'
    chrome_driver.close()


if __name__ == '__main__':
    test_bulls_cows_until_win()
