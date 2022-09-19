import pandas as pd
import rides_data as data

def main():
    data.update_pickles()
    data.print_pickles()
    data.write_assignments(pd.DataFrame([[],[5,6,7,8]]))

if __name__ == "__main__":
    main()
