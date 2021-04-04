# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# to run
# cd C:\skill_factory\253\petsfriend_api_tests\tests
# py -m pytest -v --driver Chrome --driver-path c:/skill_factory/chromedriver test_25_3.py

# @pytest.fixture()
def test_login():
    # подключаем драйвер Chrome
    pytest.driver = webdriver.Chrome('c:/skill_factory/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('vol1@test.test')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('vol1')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

    # неявное ожидание появления элемента - ссылки Мои питомцы
    wait = WebDriverWait(pytest.driver, 10).until(pytest.driver.find_element_by_css_selector('#navbarNav [href="/my_pets"]'))

    # далее - варианты попадания на страницу мои питомцы
    # плохо - только для русскоязычной версии
    # pytest.driver.find_element_by_link_text('Мои питомцы').click()
    # плохо - структура может измениться
    # pytest.driver.find_element_by_xpath('//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()
    # хорошо
    pytest.driver.find_element_by_css_selector('#navbarNav [href="/my_pets"]').click()

    # явное ожидание появления таблицы со значениями мои питомцы
    pytest.driver.implicitly_wait(10)

    # объявили глобальные переменные, чтобы заново в каждом тесте их не считать
    global all_my_pets, count_of_my_pets, count_images, names, porods, ages

    # количество строк в таблице с данными питомцев
    all_my_pets = pytest.driver.find_elements_by_xpath('//tbody/tr')

    # количество питомцев в статистике пользователя
    count_of_my_pets = pytest.driver.find_element_by_xpath('//*[h2][1]').text.split()

    # количество питомцев с фото
    count_images = len(pytest.driver.find_elements_by_tag_name('img'))

    # получаем данные из таблицы
    names = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')  #  имена
    porods = pytest.driver.find_elements_by_xpath('//tbody/tr/td[2]')  #  породы
    ages = pytest.driver.find_elements_by_xpath('//tbody/tr/td[3]')  #  возраста

    # осталось от  @pytest.fixture()
    # yield
    # pytest.driver.quit()


def test_mypets():
    # совпадает ли число моих питомцев в статистике пользователя
    # с реальным количеством строк в таблице с данными питомцев 25.3.1.1
    assert len(all_my_pets) == int(count_of_my_pets[(3)])


def test_count_img():
    # более чем у половины питомцев есть фото 25.3.1.2
    assert (count_images - 1) / len(all_my_pets) > .5


def test_names():
    # у всех имена не пустые 25.3.1.3
    for i in range(len(names)):
        assert names[i].text != ''


def test_porods():
    # у всех порода не пустые 25.3.1.3
    for i in range(len(names)):
        assert porods[i].text != ''


def test_ages():
    # у всех возаст не пустые 25.3.1.3
    for i in range(len(names)):
        assert ages[i].text != ''


def test_repeat_name():
    # У всех питомцев разные имена 25.3.1.4
    i = 0
    while i < len(names):
        j = i + 1
        while j < len(names):
            assert names[i].text != names[j].text
            j += 1
        i += 1

def test_pereat_pets():
    # В списке нет повторяющихся питомцев 25.3.1.5
    i = 0
    while i < len(names):
        j = i + 1
        while j < len(names):
            assert not (names[i].text == names[j].text and porods[i].text == porods[j].text and ages[i].text == ages[j].text)
            j += 1
        i += 1

# def test_write_to_file():
# assert len(names) == len(all_my_pets)
# f = open('workfile.txt', 'w')
# for i in range(len(names)):
#     f.write(names[i].text)
#     f.write(chr(9))
#     f.write(porods[i].text)
#     f.write(chr(9))
#     f.write(ages[i].text)
#     f.write(chr(9))
#     f.write(chr(13))
# f.close()
# assert names[0] == 'TEST_NAME'

def test_logoff():
    pytest.driver.quit()
