import sys
from PyQt5.QtWidgets import QApplication
from authenticate import createSignInDialog
from database import drop_database

if __name__ == '__main__':
    inp = int(input("Do we drop the db (0 for No, 1 for Yes): "))
    if inp == 1:
        drop_database()

    app = QApplication(sys.argv)

    signInDialog = createSignInDialog()
    signInDialog.show()
    sys.exit(app.exec_())
