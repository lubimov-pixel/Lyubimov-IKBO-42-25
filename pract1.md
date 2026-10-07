# Практическое занятие №1. Введение, основы работы в командной строке

## Задача 1
Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).
Решение:
```
Команда: ls -l /etc
Вывод:
-rw-r--r--.  1 root root       16 сен 10 13:35 adjtime
-rw-------.  1 root root     7179 мар 24  2026 afick.conf
drwxr-xr-x.  3 root root     4096 сен 10 13:21 akmods
-rw-r--r--.  1 root root     1529 июл 20  2022 aliases
-rw-r--r--.  1 root root    12288 сен 10 13:39 aliases.db
drwxr-xr-x.  3 root root     4096 сен 10 13:25 alsa
drwxr-xr-x.  2 root root     4096 сен 10 13:25 alternatives
-rw-r--r--.  1 root root      541 мар 17  2023 anacrontab
-rw-r--r--.  1 root root      269 авг 24  2023 anthy-unicode.conf
-rw-r--r--.  1 root root       55 июн 10  2024 asound.conf
-rw-r--r--.  1 root root        1 дек 28  2022 at.deny
drwxr-x---.  4 root root     4096 сен 10 13:39 audit
drwxr-xr-x.  3 root root     4096 сен 10 13:35 authselect
...
Команда: grep -o '^[^:]*' /etc/passwd |sort
Вывод:
adm
avahi
bin
chrony
colord
daemon
dbus
dnsmasq
ftp
games
geoclue
gluster
halt
lp
mail
nm-openconnect
nm-openvpn
nobody
nslcd
openvpn
operator
pipewire
polkitd
postfix
root
rpc
rtkit
sddm
shutdown
sshd
sync
systemd-coredump
systemd-oom
systemd-resolve
systemd-timesync
tcpdump
testuser
tss
unbound
user
vboxadd
```
## Задача 2
Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов, как показано в примере ниже:

```
[root@localhost etc]# cat /etc/protocols ...
142 rohc
141 wesp
140 shim6
139 hip
138 manet
```
Решение:
```
// -v - показывает строки, не совпадающие с шаблоном
//-k2 - сортировать по второму полю, -n - числовая сортировка, -r - по убыванию
grep -v '^#' /etc/protocols | sort -k2 -n -r | head -5 | awk '{print $2, $1}'   
```
## Задача 3

Написать программу banner средствами bash для вывода текстов, как в следующем примере (размер баннера должен меняться!):

```
[root@localhost ~]# ./banner "Hello from RTU MIREA!"
+-----------------------+
| Hello from RTU MIREA! |
+-----------------------+
```
Решение:
```
nano banner
Внутри команды nano:
if [ "$#" -ne 1 ]; then
    echo "Использование: $0 \"текст для баннера\"" >&2
    exit 1
fi
text="$1"
len=${#text}
line=$(printf '+%*s+' "$((len + 2))" '' | tr ' ' '-')
printf '%s\n' "$line"
printf '| %s |\n' "$text"
printf '%s\n' "$line"
Сохраняем
chmod +x banner
./banner "Hello from RTU MIREA!"
+-----------------------+
| Hello from RTU MIREA! |
+-----------------------+
shellcheck banner
```
## Задача 4


Написать программу для вывода всех идентификаторов (по правилам C/C++ или Java) в файле (без повторений).

Пример для hello.c:

```
h hello include int main n printf return stdio void world
```
Решение:
```
Создадим файл hello.c
Внутри файла:
#include <stdio.h>

void main(){
    int n = printf("hello world");
    return;
}
cd ~/Рабочий\ стол
cat hello.c
#include <stdio.h>

void main(){
    int n = printf("hello world");
    return;
}
grep -oE '[A-Za-z_][A-Za-z0-9_]*' hello.c | sort -u | tr '\n' ' ''
h hello include int main n printf return stdio void world
```
## Задача 5
Написать программу для регистрации пользовательской команды (правильные права доступа и копирование в /usr/local/bin).

Например, пусть программа называется reg:

```
./reg banner
```
Решение:
```
nano bash
Внутри nano:
#!/usr/bin/env bash
if [ "$#" -ne 1 ]; then
    printf 'Использование: %s <файл>\n' "$0" >&2
    exit 1
fi

file="$1"
if [ ! -f "$file" ]; then
    printf 'Ошибка: файл "%s" не найден\n' "$file" >&2
    exit 1
fi
chmod 755 "$file"
name=$(basename "$file")
cp "$file" "/usr/local/bin/$name"
printf 'Файл "%s" установлен в /usr/local/bin/%s с правами 755\n' "$file" "$name"
Вне nano:
chmod +x bash
sudo ./bash banner
Файл "banner" установлен в /usr/local/bin/banner с правами 755
```
## Задача 6
Написать программу для проверки наличия комментария в первой строке файлов с расширением c, js и py.
Решение:
```
nano check_bash
Внутри nano:                                                         
#!/usr/bin/env bash
if [ "$#" -lt 1 ]; then
    printf 'Использование: %s <файл> [файл ...]\n' "$0" >&2
    exit 1
fi
for file in "$@"; do
 if [ ! -f "$file" ]; then
        printf '%s: файл не найден\n' "$file" >&2
        continue
    fi
ext="${file##*.}"
if [ "$ext" != "c" ] && [ "$ext" != "js" ] && [ "$ext" != "py" ]; then
        printf '%s: пропущен (не .c, .js или .py)\n' "$file"
        continue
    fi
# Читаем первую строку
    first_line=$(head -n 1 "$file")

    # Проверяем наличие комментария в зависимости от расширения
    has_comment=0

    case "$ext" in
        c|js)
            # C и JavaScript: // или /*
            case "$first_line" in
                //*|/\**) has_comment=1 ;;
            esac
            ;;
        py)
            # Python: #
            case "$first_line" in
                \#*) has_comment=1 ;;
            esac
            ;;
    esac
if [ "$has_comment" -eq 1 ]; then
        printf '%s: комментарий есть\n' "$file"
    else
        printf '%s: комментария нет\n' "$file"
    fi
done
Вне nano:
chmod +x check_comment
cat > hello.c << 'EOF'
// Это комментарий
#include <stdio.h>
int main() { return 0; }
EOF
./check_comment hello.c
hello.c: комментарий есть
```
## Задача 7
Написать программу для нахождения файлов-дубликатов (имеющих 1 или более копий содержимого) по заданному пути (и подкаталогам).
Решение:
```
nano check_katalog
Внутри nano:
#!/usr/bin/env bash

if [ "$#" -ne 1 ] || [ ! -d "$1" ]; then
    printf 'Использование: %s <каталог>\n' "$0" >&2
    exit 1
fi
\\-exec md5sum {} + - вычисление хэшей, uniq фильтр работающий с соседними строками, -D - вывести все строки из групп, где есть дубликат
find "$1" -type f -exec md5sum {} + | sort | uniq -w32 -D
Вне nano:
chmod +x check_katalog
mkdir -p /tmp/katalog_test/sub

echo "Hello" > /tmp/katalog_test/a.txt
echo "Hello" > /tmp/katalog_test/b.txt
echo "World" > /tmp/katalog_test/sub/c.txt
echo "World" > /tmp/katalog_test/sub/d.txt
echo "Unique" > /tmp/katalog_test/unique.txt
Вывод:
09f7e02f1290be211da707a266f153b3  /tmp/katalog_test/a.txt
09f7e02f1290be211da707a266f153b3  /tmp/katalog_test/b.txt
52f83ff6877e42f613bcd2444c22528c  /tmp/katalog_test/sub/c.txt
52f83ff6877e42f613bcd2444c22528c  /tmp/katalog_test/sub/d.txt
```
## Задача 8
Написать программу, которая находит все файлы в данном каталоге с расширением, указанным в качестве аргумента и архивирует все эти файлы в архив tar.
```
nano archive_file
Внутри nano:
#!/bin/sh
if [ "$#" -ne 2 ] || [ ! -d "$1" ]; then
    printf 'Использование: %s <каталог> <расширение>\n' "$0" >&2
    exit 1
fi
dir="$1"
ext="$2"
archive="archive_${ext}_$(date +%Y%m%d_%H%M%S).tar"

# 4. Находим файлы с нужным расширением и упаковываем их в архив
#    find → список файлов через \0 (безопасно для пробелов)
#    tar  → читает список из stdin и создаёт архив
find "$dir" -type f -name "*.$ext" -print0 | tar -c --null -f "$archive" -T -
printf 'Архив "%s" создан\n' "$archive"
Вне nano:
chmod +x archive_file
mkdir -p /tmp/archive_test/sub
echo "1" > /tmp/archive_test/a.txt
echo "2" > /tmp/archive_test/b.txt
echo "3" > /tmp/archive_test/sub/c.txt
echo "4" > /tmp/archive_test/d.log
echo "5" > "/tmp/archive_test/my file.txt"
./archive_file /tmp/archive_test txt
tar: Удаляется начальный `/' из имен объектов
tar: Удаляются начальные `/' из целей жестких ссылок
Архив "archive_txt_20261001_002238.tar" создан
```
## Задача 9
Написать программу, которая заменяет в файле последовательности из 4 пробелов на символ табуляции. Входной и выходной файлы задаются аргументами.
Решение:
```
nano replace_spaces
Внутри nano:
#!/usr/bin/env bash
if [ "$#" -ne 2 ]; then
    printf 'Использование: %s <входной_файл> <выходной_файл>\n' "$0" >&2
    exit 1
fi
input="$1"
output="$2"
if [ ! -r "$input" ]; then
    printf 'Ошибка: файл "%s" не найден или недоступен для чтения\n' "$input" >&2
    exit 1
fi
sed 's/    /\t/g' "$input" > "$output"
printf 'Файл "%s" обработан, результат в "%s"\n' "$input" "$output"
Вне nano:
chmod +x replace_spaces
cat > input.txt << 'EOF'
    int x = 5;
        print(x);
no spaces here
  two spaces
     five spaces
            eight spaces
EOF
./replace_spaces input.txt output.txt
Файл "input.txt" обработан, результат в "output.txt"
cat output.txt
Результат:
       int x = 5;
                print(x);
no spaces here
  two spaces
         five spaces
                        eight spaces
```
## Задача 10
Написать программу, которая выводит названия всех пустых текстовых файлов в указанной директории. Директория передается в программу параметром.
Решение:
```
nano find_empty
Внутри nano:
#!/usr/bin/env bash
if [ "$#" -ne 1 ]; then
    printf 'Использование: %s <каталог>\n' "$0" >&2
    exit 1
fi
dir="$1"
# 2. Проверяем, что это существующий каталог
if [ ! -d "$dir" ]; then
    printf 'Ошибка: "%s" не является каталогом\n' "$dir" >&2
    exit 1
fi
find "$dir" -type f -empty -print
Вне nano:
chmod +x find_empty
mkdir -p /tmp/empty_test/sub
touch /tmp/empty_test/empty1.txt
touch /tmp/empty_test/empty2.log
touch /tmp/empty_test/sub/empty3.txt
echo "text" > /tmp/empty_test/not_empty.txt
echo "x" > /tmp/empty_test/sub/also_not_empty.txt
mkdir /tmp/empty_test/empty_dir
./find_empty /tmp/empty_test
/tmp/empty_test/empty1.txt
/tmp/empty_test/empty2.log
/tmp/empty_test/sub/empty3.txt
```
