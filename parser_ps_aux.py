from subprocess import (
    call
)


def check_output_example():
    with open("oc.txt", 'w') as txt:
        call(["ps", "aux"], stdout=txt)

    with open("oc.txt", 'r') as txt:
        txt.readline()
        statistics_file = txt.readlines()
        system_lst = []
        users = []
        pid = 0
        CPU = 0.0
        MEM = 0.0
        process_counter = {}
        RSS = 0.0
        MAX_RSS = 0.0
        MAX_RSS_PROCESS = ''
        MAX_CPU = 0.0
        MAX_CPU_PROCESS = ''
        for i in statistics_file:
            j = i.split()
            if j[0] not in users:
                users.append(j[0])
                process_counter[j[0]] = 1
            process_counter[j[0]] += 1
            system_lst.append(j)
            pid += 1
            CPU += float(j[2])
            MEM += float(j[3])
            RSS += float(j[5])
            if float(j[5]) > MAX_RSS:
                MAX_RSS = float(j[5])
                MAX_RSS_PROCESS = str(j[10])
            if float(j[2]) > MAX_CPU:
                MAX_CPU = float(j[2])
                MAX_CPU_PROCESS = str(j[10])

        with open('ps_aux_result.txt', 'w') as result:
            print(f'Пользователи системы: {users}', file=result)
            print(f'Процессов всего: {pid}', file=result)
            print(f'CPU %: {CPU}', file=result)
            print(f'Memory %: {MEM}', file=result)
            print(f'Процессов для каждого пользователя:  {process_counter}', file=result)
            print(f'Всего MEMORY: {RSS}', file=result)
            print(f'Больше всего используется MEMORY: <<{MAX_RSS_PROCESS}>>: память = {MAX_RSS}', file=result)
            print(f'Больше всего используется CPU: <<{MAX_CPU_PROCESS}>>: % = {MAX_CPU}', file=result)

        with open('ps_aux_result.txt', 'r') as result:
            for i in result:
                print(result.read())


if __name__ == '__main__':
    check_output_example()
