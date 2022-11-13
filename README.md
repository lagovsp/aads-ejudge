# АиСД МГТУ ИУ8 Осень 2022 (Ejudge)

## Тестирование

Для тестирования своих решений можно использовать `check.sh` из папки `scripts`.
Для этого скопируйте файлы `checker.py` и `check.sh` в одну директорию и введите команду
`./check.sh <solution.py> <tests-folder> <tests-number>`, где

- `<solution.py>` - название вашего скрипта на Python
  (или путь до него относительно `check.sh`, если скопированные файлы находятся в другой директории)
- `<tests-folder>` - путь до папки с тестами к вашему заданию.
  В этой папке должны находится папки `dat` и `ans` с вводом тестов
  и ответами к ним соответственно (см. пример в репозитории)
- `<tests-number>` - количество тестов. Будут прогоняться все тесты в диапазоне `[0;N]`
  (от `1.dat` до `N.dat`). Ничего страшного,
  если некоторых тестов из диапазона не будет, - они будут проигнорированы

![Screenshot](assets/checker-sample.png)

###### Автор: Сергей Лагов
###### Внесли вклад: Андрей Николаев, Иван Алферов, Богдан Шумилишский
