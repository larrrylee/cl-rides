from assignments import assign
import rides_data as data

def main():
    #data.update_pickles()
    #data.print_pickles()
    (drivers, riders) = data.get_cached_data()
    data.clean_data(drivers, riders)
    out = assign(drivers, riders)
    print(out)


if __name__ == "__main__":
    main()
