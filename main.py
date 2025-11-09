import App.view as view

# Solucionar problemas de buffer
import csv
csv.field_size_limit(2147483647)
# Limite que la guía recomienda cambiar
import sys
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

# Main function
def main():
    view.main()


# Main function call to run the program
if __name__ == '__main__':
    main()
