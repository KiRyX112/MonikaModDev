import os, shutil

# нет папки "spritepacks"? (грустное лицо Мегамозга)
if not "spritepacks" in os.listdir("../"):
    print("Папка со спрайтпаками не обнаружена.")
    quit()

# нужная нам папка есть, идём дальше
# P.S.: файлы из папки "unreleased" не будут добавлены,
# т.к. название самой папки уже говорит всё за себя,
# а нам лишний вес конечного дистрибутива ни к чему 
for x in os.listdir("../spritepacks/released"):
    for u in os.listdir(f"../spritepacks/released/{x}"):
        shutil.copytree(f"../spritepacks/released/{x}/{u}/mod_assets", "../Monika After Story/game/mod_assets", dirs_exist_ok=True)

print("Работяга отработал свою смену. Остальное за тобой. 💪")
input("Нажми Enter или Закрыть для закрытия этого окна.")
