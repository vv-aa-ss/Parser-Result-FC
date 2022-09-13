from time import sleep
import requests
from bs4 import BeautifulSoup
from settings import *
import subprocess
import os


def get_result(item):
    result = ""
    src = requests.get(f"{item}", proxies=proxies, headers=headers)
    src = src.json()
    print(".", end="")
    for item in src["ajax-updater"]["params"]["html"][0]:
        try:
            if 6 < int(item) < 10:
                soup = BeautifulSoup(src["ajax-updater"]["params"]["html"][0][f"{item}"], "lxml")
                rows = soup.find_all(
                    class_="sport-table__row sport-table__row_align-items_center sport-table__row_gap_s "
                           "sport-table__row_border_yes")
                for item in rows:
                    # Дата и время
                    date_m = item.find(class_="sport-table__cell sport-table__cell_space_xl").find_all(
                        class_="sport-table__row")[0].text
                    time_m = item.find(class_="sport-table__cell sport-table__cell_space_xl").find_all(
                        class_="sport-table__row")[1].text

                    # Команда 1
                    if item.find(class_="sport-table__cell sport-table__cell_align_right sport-table__cell_flex_yes "
                                        "sport-table__cell_space_l sport-table__cell_type_hide-score-unbold "
                                        "sport-table__cell_ellipsis_yes"):
                        command_1 = item.find(class_="sport-table__cell sport-table__cell_align_right "
                                                     "sport-table__cell_flex_yes sport-table__cell_space_l "
                                                     "sport-table__cell_type_hide-score-unbold "
                                                     "sport-table__cell_ellipsis_yes").text
                    else:
                        command_1 = item.find(class_="sport-table__cell sport-table__cell_align_right "
                                                     "sport-table__cell_bold_yes sport-table__cell_flex_yes "
                                                     "sport-table__cell_space_l sport-table__cell_type_hide-score-unbold "
                                                     "sport-table__cell_ellipsis_yes").text
                    # Счет
                    if item.find(class_="sport-duel__info-real-score sport-duel__info-real-score_size_m"):
                        count = item.find(class_="sport-duel__info-real-score sport-duel__info-real-score_size_m").text
                    else:
                        count = item.find(
                            class_="text-container text-container_ellipsis_yes typo typo_text_l typo_line_m "
                                   "colorize-72hy61").text

                    # Команда 2
                    if item.find(
                            class_="sport-table__cell sport-table__cell_flex_yes sport-table__cell_type_hide-score-unbold "
                                   "sport-table__cell_ellipsis_yes"):
                        command_2 = item.find(
                            class_="sport-table__cell sport-table__cell_flex_yes sport-table__cell_type_hide-score-unbold "
                                   "sport-table__cell_ellipsis_yes").text
                    else:
                        command_2 = item.find(
                            class_="sport-table__cell sport-table__cell_bold_yes sport-table__cell_flex_yes "
                                   "sport-table__cell_type_hide-score-unbold sport-table__cell_ellipsis_yes").text
                    result += f"{date_m.strip().ljust(9)} {time_m.strip().ljust(5)} || {command_1.strip().rjust(23)} {count.strip().center(7)} {command_2.strip().ljust(23)}\n"
        except Exception as ex:
            continue
    return result


def main():
    main_result = "-----------------------------"
    for items in country.items():
        print(f"[INFO]  Getting ->> {items[0].ljust(15)}" + "...", end="")
        """Забираем JSON"""
        main_result += f"\n--------{items[0]}\n"
        main_result += (get_result(items[1]))
        main_result += "------------------------------"
        print(".", end="")
        print("...Ok")
    show_and_del(main_result)


def show_and_del(text):
    # Пишем в файл
    with open(f"temp.txt", "w", encoding="utf-8") as file:
        file.write(text)
    try:
        # Удаляем его после закрытия окна
        sleep(2)
        print(subprocess.getoutput(f'{os.getcwd()}\\temp.txt'))
        os.remove(f'{os.getcwd()}\\temp.txt')
    except Exception as ex:
        print(ex)
    finally:

        print("Exit Programm. Good Bye")
        sleep(2)


if __name__ == "__main__":
    main()
