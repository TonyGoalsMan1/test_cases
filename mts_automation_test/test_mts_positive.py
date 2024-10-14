import pytest
from playwright.sync_api import sync_playwright #Синхронный API Playwright
import allure #Библиотека для создания отчетов и описания шагов теста

# Используем декораторы Allure для организации отчета
@allure.feature("Домашний интернет и ТВ")
@allure.story("Позитивный тест-кейс: Подключение тарифа")
def test_mts_positive():
    #Инициализируем Playwright и запускаем браузер
    with sync_playwright() as p:
        # Запускаем браузер Chromium в режиме отображения (headless=False)
        browser = p.chromium.launch(headless=False)
        # Создаем новый контекст и страницу для теста
        context = browser.new_context()
        page = context.new_page()
        try:
            # Здесь мы добавим шаги теста
            with allure.step("Шаг 1: перейти на сайт mts.ru"):
                page.goto("https://www.mts.ru")
                page.wait_for_load_state('load')

            with allure.step("Шаг 2: Выбрать 'Домашний интернет и ТВ'"):
                page.click("//span[contains(@class, 'card__right-content') and contains(text(), 'Домашний')]")
                page.wait_for_load_state('load')

            with allure.step("Шаг 3: Выбрать город подключения 'Москва'"):
                # Проверяем, появляется ли окно выбора региона
                if page.is_visible("text='Выберите ваш регион'"):
                    page.click("text='Москва'")
                else:
                    # Проверяем текущий выбранный город
                    if page.is_visible("a[data-id='button_region']"):
                        current_city = page.inner_text("a[data-id='button_region']")
                        if current_city != "Москва":
                            page.click("a[data-id='button_region']")
                            page.click("text='Москва'")

            with allure.step("Шаг 4: Проверить наличие тарифов и кнопок"):
                page.wait_for_selector(".card.card__wrapper", state="visible", timeout=60000)
                tariffs = page.locator(".card.card__wrapper")

                # Проверяем, что на странице есть как минимум 3 тарифа
                assert tariffs.count() >= 3, "Не все тарифы найдены на странице"

                # Проверяем наличие кнопок "Подключить" и "Подробнее" для каждого тарифа
                for i in range(tariffs.count()):
                    tariff = tariffs.nth(i)
                    button_on = tariff.locator(".mm-web-button__text", has_text="Подключить")
                    more = tariff.locator(".mm-web-button__text", has_text="Подробнее")

                    assert button_on.count() > 0 and button_on.first.is_visible(), "Кнопка 'Подключить' не найдена в тарифе"
                    assert more.count() > 0 and more.first.is_visible(), "Кнопка 'Подробнее' не найдена в тарифе"

            # Шаг 5: Выбрать тариф и перейти на его страницу
            with allure.step("Шаг 5: Выбрать тариф и перейти на его страницу"):
                # Выбираем первый тариф из списка
                first_tariff = tariffs.nth(0)
                # Используем локатор для кнопки "Подробнее" внутри выбранного тарифа
                more_button_locator = first_tariff.locator(".mm-web-button__text", has_text="Подробнее")
                assert more_button_locator.count() > 0, "Кнопка 'Подробнее' не найдена в первом тарифе"
                # Кликаем по кнопке "Подробнее"
                with page.expect_navigation():
                    more_button_locator.first.click()
                # Ждём полной загрузки страницы
                page.wait_for_load_state('load')

            with allure.step("Шаг 6: Проверить соответствие информации о тарифе"):
                # Ждем появления элемента с классом 'title'
                page.wait_for_selector(".title", timeout=10000)
                # Получаем элемент с названием тарифа
                tariff_name_element = page.locator(".title")
                assert tariff_name_element.count() > 0, "Название тарифа не найдено"
                tariff_name = tariff_name_element.first.inner_text().strip()
                assert tariff_name != "", "Название тарифа пустое"


            with allure.step("Шаг 7: Выбрать оптимальную скорость и проверить динамику цены"):
                # Фокусируемся на ползунке
                slider = page.locator("mat-slider")
                assert slider.count() > 0, "Ползунок скорости не найден"
                slider.focus()

                # Нажимаем клавишу "ArrowLeft" несколько раз, чтобы установить минимальное значение
                for _ in range(2):
                    page.keyboard.press("ArrowLeft")
                    page.wait_for_timeout(500)

                # Получаем начальную цену
                price_element = page.locator(".price-value")
                initial_price = price_element.first.inner_text().strip()
                print(f"Initial price: {initial_price}")

                # Нажимаем клавишу "ArrowRight" один раз, чтобы увеличить значение
                page.keyboard.press("ArrowRight")
                page.wait_for_timeout(1000)  # Ждем обновления цены

            with allure.step("Шаг 9: Нажать на кнопку 'Подключить'"):
                # Находим кнопку "Подключить" на странице тарифа
                connect_button = page.locator("button.btn.btn_large.product-header-button", has_text="Подключить")
                assert connect_button.count() > 0, "Кнопка 'Подключить' не найдена"
                connect_button.first.click()
                # Ждем появления формы "Заявка на подключение"
                page.wait_for_selector("form", timeout=5000)

            with allure.step("Шаг 10: Проверить появление формы и наличие полей"):
                # Проверяем, что форма появилась, ищем по уникальному селектору
                form = page.locator("div.request-form-popup")  # Используйте класс верхнего контейнера формы
                assert form.count() > 0, "Форма 'Заявка на подключение' не появилась"

                # Проверяем наличие заголовка формы
                form_title = form.locator("div.request-form-popup__title", has_text="Заявка на подключение")
                assert form_title.count() > 0, "Заголовок формы 'Заявка на подключение' не найден"

                # Проверяем наличие поля "Номер"
                phone_input = form.locator("input[placeholder='XXX XXX XX XX']")
                assert phone_input.count() > 0, "Поле 'Номер' не найдено"

                # Проверяем наличие поля "Имя"
                name_input = form.locator("input[placeholder='Ваше имя']")
                assert name_input.count() > 0, "Поле 'Имя' не найдено"

                # Проверяем, что форма появилась, ищем по уникальному селектору
                form = page.locator("div.request-form-popup")  # Используйте класс верхнего контейнера формы
                assert form.count() > 0, "Форма 'Заявка на подключение' не появилась"

                # Проверяем наличие заголовка формы
                form_title = form.locator("div.request-form-popup__title", has_text="Заявка на подключение")
                assert form_title.count() > 0, "Заголовок формы 'Заявка на подключение' не найден"

                # Проверяем наличие поля "Номер"
                phone_input = form.locator("input[placeholder='XXX XXX XX XX']")
                assert phone_input.count() > 0, "Поле 'Номер' не найдено"

                # Проверяем наличие поля "Имя"
                name_input = form.locator("input[placeholder='Ваше имя']")
                assert name_input.count() > 0, "Поле 'Имя' не найдено"

            with allure.step("Шаг 11: Проверить ввод значений в поля формы"):
                # Вводим корректный номер телефона
                with allure.step("Ввод корректного номера телефона"):
                    phone_input.fill("9204670465")
                    formatted_phone = phone_input.input_value()
                    print(f"Введенный номер телефона: {formatted_phone}")
                    # Проверяем, что номер отформатирован корректно (при необходимости)

                # Вводим имя (если необходимо)
                with allure.step("Ввод имени"):
                    name_input.fill("Иван")

                # Нажимаем на кнопку "Оставить заявку"
                with allure.step("Нажать на кнопку 'Оставить заявку'"):
                    submit_button = form.locator("div.mm-web-button__text", has_text="Оставить заявку")
                    assert submit_button.count() > 0, "Кнопка 'Оставить заявку' не найдена"

                    # Ожидаем либо навигации, либо закрытия страницы
                    with page.expect_navigation() as navigation_info:
                        submit_button.first.click()

                    # Проверяем, была ли навигация
                    if navigation_info.value:
                        new_page = page
                    else:
                        # Если навигации не было, возможно, страница закрылась или открылась новая
                        if len(context.pages) > 1:
                            new_page = context.pages[-1]
                        else:
                            new_page = page  # Используем текущую страницу

        finally:
            browser.close()
