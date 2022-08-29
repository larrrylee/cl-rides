import rides_input_data as data

FINAL_SHEET_KEY = "15KJPVqZT6pMq8Qg4qufx9iZOArzjxeD_MN-A-ka6Jnk"

def main():
    data.update_pickles()
    data.print_pickles()

if __name__ == "__main__":
    main()
